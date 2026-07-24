from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from datetime import datetime
import secrets
from functools import wraps
from __init__ import Company_news, Company_user
from __init__ import Session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# ==================== 装饰器 ====================

def login_user_required(f):
    """用户登录校验装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated


def login_admin_required(f):
    """管理员登录校验装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"code": 403, "msg": "你不是管理员,你没有该权限"}), 403
        return f(*args, **kwargs)
    return decorated


# ==================== 页面渲染路由 ====================

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """登录页面"""
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    db = Session()
    user = db.query(Company_user).filter(Company_user.username == username).first()
    db.close()
    if user and user.password == password:
        session['username'] = username
        session['role'] = user.role
        return redirect(url_for('index'))
    return render_template('login.html', error='用户名或密码错误')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """注册页面"""
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    role = request.form.get('role', 'user')
    db = Session()
    existing_user = db.query(Company_user).filter(Company_user.username == username).first()
    if existing_user:
        db.close()
        return render_template('register.html', error='用户名已存在')
    user = Company_user(username=username, password=password, role=role)
    db.add(user)
    db.commit()
    db.close()
    return render_template('register.html', msg='注册成功，请登录')


@app.route('/logout')
def logout_page():
    """退出登录"""
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/')
@login_user_required
def index():
    """首页：公司介绍 + 最近3条新闻"""
    db = Session()
    news_db = db.query(Company_news).order_by(Company_news.id.desc()).all()
    news_list = [{"id": n.id, "title": n.title, "content": n.content,
                  "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
                 for n in news_db[:3]]
    db.close()
    return render_template('index.html', news_list=news_list)


@app.route('/news')
@login_user_required
def news_list_page():
    """新闻列表页"""
    db = Session()
    news_db = db.query(Company_news).order_by(Company_news.id.desc()).all()
    news_list = [{"id": n.id, "title": n.title, "content": n.content,
                  "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
                 for n in news_db]
    db.close()
    return render_template('news_list.html', news_list=news_list)


@app.route('/news/<int:id>')
@login_user_required
def news_detail_page(id):
    """新闻详情页"""
    db = Session()
    news = db.query(Company_news).filter(Company_news.id == id).first()
    if not news:
        db.close()
        return "新闻不存在", 404
    result = {"id": news.id, "title": news.title, "content": news.content,
              "category": news.category, "date": news.date.strftime("%Y-%m-%d %H:%M:%S")}
    db.close()
    return render_template('news_detail.html', news=result)


@app.route('/admin')
@login_user_required
@login_admin_required
def admin_page():
    """后台管理页面"""
    db = Session()
    news_db = db.query(Company_news).order_by(Company_news.id.desc()).all()
    news_list = [{"id": n.id, "title": n.title, "content": n.content,
                  "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
                 for n in news_db]
    db.close()
    return render_template('admin.html', news_list=news_list)


@app.route('/admin/create', methods=['POST'])
@login_user_required
@login_admin_required
def admin_create_news():
    """后台发布新闻（表单提交）"""
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    category = request.form.get('category', '')
    if not title or not content or not category:
        return redirect(url_for('admin_page'))
    db = Session()
    news = Company_news(title=title, content=content, category=category, date=datetime.now())
    db.add(news)
    db.commit()
    db.close()
    return render_template('admin.html', msg='发布成功',
                           news_list=_get_news_list_for_admin())


@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_user_required
@login_admin_required
def admin_delete_news(id):
    """后台删除新闻"""
    db = Session()
    news = db.query(Company_news).filter(Company_news.id == id).first()
    if news:
        db.delete(news)
        db.commit()
    db.close()
    return render_template('admin.html', msg='删除成功',
                           news_list=_get_news_list_for_admin())


@app.route('/admin/clear', methods=['POST'])
@login_user_required
@login_admin_required
def admin_clear_news():
    """后台清空所有新闻"""
    db = Session()
    db.query(Company_news).delete()
    db.commit()
    db.close()
    return render_template('admin.html', msg='已清空所有新闻',
                           news_list=_get_news_list_for_admin())


def _get_news_list_for_admin():
    """复用：获取新闻列表字典（供管理页面刷新用）"""
    db = Session()
    news_db = db.query(Company_news).order_by(Company_news.id.desc()).all()
    news_list = [{"id": n.id, "title": n.title, "content": n.content,
                  "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
                 for n in news_db]
    db.close()
    return news_list


# ==================== API 路由（保留，兼容 Postman 测试） ====================

@app.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    db = Session()
    user = db.query(Company_user).filter(Company_user.username == username).first()
    db.close()
    if user and user.password == password:
        session['username'] = username
        session['role'] = user.role
        return jsonify({"code": 200, "msg": "登录成功"})
    else:
        return jsonify({"code": 400, "msg": "用户名或密码错误"}), 400


@app.route("/auth/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']
    db = Session()
    existing_user = db.query(Company_user).filter(Company_user.username == username).first()
    if existing_user:
        db.close()
        return jsonify({"code": 400, "msg": "用户名已存在"}), 400
    user = Company_user(username=username, password=password, role=role)
    db.add(user)
    db.commit()
    db.close()
    return jsonify({"code": 200, "msg": "注册成功"})


@app.route('/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"code": 200, "msg": "退出成功"})


@app.route('/auth/admin/create_news', methods=['POST'])
@login_user_required
@login_admin_required
def api_create_news():
    data = request.get_json()
    if not data.get('title') or not data.get('content') or not data.get('category'):
        return jsonify({"code": 400, "msg": "请填写完整信息"}), 400
    db = Session()
    news = Company_news(title=data['title'], content=data['content'],
                        category=data['category'], date=datetime.now())
    db.add(news)
    db.commit()
    result = {"id": news.id, "title": news.title, "content": news.content,
              "category": news.category, "date": news.date.strftime("%Y-%m-%d %H:%M:%S")}
    db.close()
    return jsonify({"code": 200, "msg": "创建新闻成功", "news": result}), 201


@app.route('/auth/admin/get_news', methods=['GET'])
@login_user_required
def api_get_all_news():
    db = Session()
    news_db = db.query(Company_news).all()
    result = [{"id": n.id, "title": n.title, "content": n.content,
               "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
              for n in news_db]
    db.close()
    return jsonify({"code": 200, "msg": "获取新闻列表成功", "news": result}), 200


@app.route('/auth/admin/get_news/<int:id>', methods=['GET'])
@login_user_required
def api_get_news(id):
    db = Session()
    news_db = db.query(Company_news).filter(Company_news.id == id).first()
    if not news_db:
        db.close()
        return jsonify({"code": 404, "msg": "新闻不存在"}), 404
    result = {"id": news_db.id, "title": news_db.title, "content": news_db.content,
              "category": news_db.category, "date": news_db.date.strftime("%Y-%m-%d %H:%M:%S")}
    db.close()
    return jsonify({"code": 200, "msg": "获取新闻成功", "news": result}), 200


@app.route('/auth/admin/delete_news/<int:id>', methods=['DELETE'])
@login_user_required
@login_admin_required
def api_delete_news(id):
    db = Session()
    news_db = db.query(Company_news).filter(Company_news.id == id).first()
    if not news_db:
        return jsonify({"code": 404, "msg": "新闻不存在"}), 404
    db.delete(news_db)
    db.commit()
    db.close()
    return jsonify({"code": 200, "msg": "删除新闻成功"}), 200


@app.route('/auth/admin/clear_news', methods=['DELETE'])
@login_user_required
@login_admin_required
def api_clear_news():
    db = Session()
    db.query(Company_news).delete()
    db.commit()
    db.close()
    return jsonify({"code": 200, "msg": "清空所有新闻成功"}), 200


@app.route('/auth/admin/home', methods=['GET'])
@login_user_required
def api_home():
    db = Session()
    news_db = db.query(Company_news).all()
    result = [{"id": n.id, "title": n.title, "content": n.content,
               "category": n.category, "date": n.date.strftime("%Y-%m-%d %H:%M:%S")}
              for n in news_db[-3:]]
    db.close()
    return jsonify({"code": 200, "msg": "首页展示成功",
                    "intro": "这是一个公司介绍", "news": result}), 200


if __name__ == '__main__':
    print("=" * 50)
    print("  科技公司 CMS 系统")
    print("  前端页面: http://127.0.0.1:5002/")
    print("  API 接口: http://127.0.0.1:5002/auth/")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5002)
