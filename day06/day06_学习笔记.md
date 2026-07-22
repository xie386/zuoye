# Day06 学习笔记：Python 数据库操作 —— PyMySQL & SQLAlchemy

---

## 目录

1. [PyMySQL 原生驱动封装](#1-pymysql-原生驱动封装)
2. [SQLAlchemy 入门与连接](#2-sqlalchemy-入门与连接)
3. [数据表模型定义（ORM 映射）](#3-数据表模型定义orm-映射)
4. [CRUD 操作详解](#4-crud-操作详解)
5. [高级查询：排序、分页、模糊查询](#5-高级查询排序分页模糊查询)
6. [聚合统计（func 函数）](#6-聚合统计func-函数)
7. [事务管理与异常回滚](#7-事务管理与异常回滚)
8. [异步 SQLAlchemy（aiomysql）](#8-异步-sqlalchemyaiomysql)
9. [封装工具类实战](#9-封装工具类实战)
10. [同步 vs 异步性能对比实战](#10-同步-vs-异步性能对比实战)
11. [异步 CRUD 完整工具类封装](#11-异步-crud-完整工具类封装)
12. [综合实战：学生信息管理系统](#12-综合实战学生信息管理系统)
13. [知识点速查表](#13-知识点速查表)

---

## 1. PyMySQL 原生驱动封装

### 1.1 什么是 PyMySQL？

PyMySQL 是 Python 连接 MySQL 的原生驱动，通过它可以直接执行 SQL 语句，不依赖 ORM 框架。适合简单场景或学习 SQL 底层原理。

### 1.2 安装

```bash
pip install pymysql
```

### 1.3 封装工具类

```python
import pymysql

class MySqlLUtil:
    """
    MySQL 工具类，封装连接、查询、执行、关闭等操作
    """

    def __init__(self, host='localhost', port=3306, user='root', password='123456', db='test'):
        """
        初始化数据库连接

        参数:
            host: 数据库主机地址，默认 localhost
            port: 端口号，MySQL 默认 3306
            user: 用户名
            password: 密码
            db: 数据库名
            charset: 字符集，推荐 utf8mb4 支持 emoji
        """
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4'
        )
        # 创建游标，用于执行 SQL 并获取结果
        self.cursor = self.conn.cursor()

    def query(self, sql, args=None):
        """
        查询方法，自动判断返回单条还是多条结果

        判断逻辑：
        - SQL 中包含 COUNT()、SUM()、AVG()、MAX()、MIN() 或 LIMIT 1 → fetchone()
        - 否则 → fetchall()

        参数:
            sql: SQL 查询语句
            args: 参数化查询的参数，用于防 SQL 注入

        返回:
            单条查询: 元组 (tuple)
            多条查询: 元组列表 list[tuple]
        """
        # 执行 SQL，args or [] 防止传 None 时报错
        self.cursor.execute(sql, args or [])

        # 转为大写并去除首尾空格，方便判断
        sql_upper = sql.upper().strip()

        # any(): 只要列表中任意一个条件为 True 就返回 True
        # 聚合函数和 LIMIT 1 通常只返回单条结果
        is_single = any(kw in sql_upper for kw in [
            'COUNT(', 'SUM(', 'AVG(', 'MAX(', 'MIN(', 'LIMIT 1'
        ])

        # 三元表达式：单条用 fetchone，多条用 fetchall
        return self.cursor.fetchone() if is_single else self.cursor.fetchall()

    def execute(self, sql, args=None):
        """
        执行非查询 SQL（INSERT、UPDATE、DELETE 等）

        参数:
            sql: SQL 语句
            args: 参数化参数

        返回:
            rowcount: 受影响的行数 (int)
            注意：rowcount 是属性不是方法，不能加括号()
        """
        self.cursor.execute(sql, args or [])
        self.conn.commit()           # 提交事务
        return self.cursor.rowcount  # 返回受影响行数

    def close(self):
        """关闭游标和连接，释放资源"""
        self.cursor.close()
        self.conn.close()


# ========== 使用示例 ==========
if __name__ == '__main__':
    # 连接指定数据库
    util = MySqlLUtil(db='ZQK4')

    # 查询所有学生 → fetchall()
    print(util.query('select * from student'))

    # 统计学生人数 → fetchone()
    print(util.query('select count(*) from student'))

    util.close()
```

> **关键 API 说明：**
>
> | 方法 | 作用 | 返回值 |
> |------|------|--------|
> | `pymysql.connect()` | 创建数据库连接 | Connection 对象 |
> | `conn.cursor()` | 创建游标 | Cursor 对象 |
> | `cursor.execute(sql, args)` | 执行 SQL | 受影响行数 |
> | `cursor.fetchone()` | 获取一条结果 | 元组 |
> | `cursor.fetchall()` | 获取所有结果 | 元组列表 |
> | `conn.commit()` | 提交事务 | 无 |
> | `cursor.rowcount` | 受影响行数（属性） | int |
> | `cursor.close()` | 关闭游标 | 无 |
> | `conn.close()` | 关闭连接 | 无 |

---

## 2. SQLAlchemy 入门与连接

### 2.1 什么是 SQLAlchemy？

SQLAlchemy 是 Python 最流行的 **ORM（对象关系映射）** 框架。它可以让你用 Python 类来操作数据库表，而不需要手写原始 SQL。

> **ORM 核心思想：** 类 → 表，对象 → 行，属性 → 字段。

### 2.2 安装

```bash
pip install sqlalchemy pymysql
```

### 2.3 创建引擎与连接

```python
from sqlalchemy import create_engine, text       # text: 包裹原生 SQL
from sqlalchemy.orm import sessionmaker, declarative_base

# ============ 1. 创建数据库引擎 ============
# 连接字符串格式：数据库类型+驱动://用户名:密码@主机:端口/数据库名
engine = create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4',
    echo=True   # echo=True: 在控制台打印所有执行的 SQL 语句，方便调试
)

# ============ 2. 创建 ORM 基类 ============
# 所有模型类都必须继承这个 Base
Base = declarative_base()

# ============ 3. 创建会话工厂 ============
# autoflush=False: 禁用自动刷新（手动控制何时发送 SQL）
# autocommit=False: 禁用自动提交（手动 commit）
# bind=engine: 绑定数据库引擎
SessionLoc = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# ============ 4. 创建会话实例 ============
db = SessionLoc()

# ============ 5. 执行原生 SQL（需要用 text() 包裹） ============
result = db.execute(text('select * from student'))
print(result.fetchall())

# ============ 6. 关闭连接 ============
db.close()
```

> **SQLAlchemy 2.0 重要变化：**
>
> - 原生 SQL 必须用 `text()` 包裹，否则报错：`ArgumentError: Textual SQL expression should be explicitly declared as text()`
> - `declarative_base` 建议从 `sqlalchemy.orm` 导入（2.0 已弃用 `sqlalchemy.ext.declarative` 路径）

### 2.4 架构层次图

```
┌─────────────────────────────────────┐
│         你的 Python 代码             │
├─────────────────────────────────────┤
│  Session (会话层) — 增删改查的入口   │
├─────────────────────────────────────┤
│  Engine (引擎层) — 管理连接池         │
├─────────────────────────────────────┤
│  DBAPI (驱动层) — pymysql/aiomysql   │
├─────────────────────────────────────┤
│  MySQL 数据库                        │
└─────────────────────────────────────┘
```

---

## 3. 数据表模型定义（ORM 映射）

### 3.1 定义学生表模型

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# 引擎和基类（复用前面代码）
engine = create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4', echo=True
)
Base = declarative_base()
SessionLoc = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Student(Base):
    """
    学生表模型
    - 类名 Student → 表名 students（默认蛇形命名）
    - 通过 __tablename__ 可以自定义表名
    """
    __tablename__ = 'students'

    id = Column(
        Integer,                          # 字段类型：整数
        primary_key=True,                 # 主键
        autoincrement=True,               # 自增（MySQL 默认行为）
        comment='主键'                    # 字段注释
    )

    name = Column(
        String(20),                       # 字符串，最大长度 20
        nullable=False,                   # 不允许为空
        comment='姓名'
    )

    age = Column(
        Integer,
        nullable=False,
        default=18,                       # 默认值
        comment='年龄'
    )

    gender = Column(
        String(10),
        default='未知',
        comment='性别'
    )

    score = Column(
        Float,                            # 浮点数
        default=0.0,
        comment='成绩'
    )

    create_time = Column(
        DateTime,
        default=datetime.now,             # 默认当前时间
        comment='创建时间'
    )

# ============ 建表 ============
# 将所有继承 Base 的模型类同步到数据库
Base.metadata.create_all(engine)
print("数据库表创建成功")
```

### 3.2 定义班级表模型

```python
class Class(Base):
    """
    班级表模型
    注意：类名 Class，表名用 class_table 避免关键字冲突
    """
    __tablename__ = 'class_table'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    class_name = Column(
        String(20),
        nullable=False,
        unique=True,          # 唯一约束，班级名不能重复
        comment='班级名'
    )
    teacher = Column(String(20), nullable=False, comment='班主任')
    student_num = Column(Integer, default=0, comment='人数')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
```

### 3.3 Column 常用参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `primary_key=True` | 设为主键 | `id` |
| `autoincrement=True` | 自增（MySQL 默认开启） | `id` |
| `nullable=False` | 不允许为空 | `name` |
| `default=值` | 设置默认值 | `default=18` |
| `unique=True` | 唯一约束 | `class_name` |
| `comment='说明'` | 字段注释 | `comment='姓名'` |

### 3.4 常用 Column 类型

| 类型 | Python 对应 | 数据库对应 |
|------|-------------|------------|
| `Integer` | `int` | INT |
| `String(n)` | `str` | VARCHAR(n) |
| `Float` | `float` | FLOAT |
| `Text` | `str` | TEXT（长文本） |
| `DateTime` | `datetime` | DATETIME |
| `Boolean` | `bool` | TINYINT |

---

## 4. CRUD 操作详解

CRUD 代表数据库四大基本操作：Create（增）、Read（查）、Update（改）、Delete（删）。

### 4.1 新增（Create）

```python
# 方式一：创建对象后 add
stu1 = Student(name='张三', age=18, gender='男', score=85.0)
db.add(stu1)    # 添加到会话（此时未写入数据库）

# 方式二：批量添加
stu2 = Student(name='李四', age=19, gender='女', score=90.0)
stu3 = Student(name='王五', age=20, gender='男', score=78.0)
db.add_all([stu2, stu3])   # 批量添加

# 提交事务，真正写入数据库
db.commit()
```

> **关键点：**
> - `db.add()` 只是将对象加入 SQLAlchemy 的会话跟踪
> - `db.commit()` 才是真正把数据写入数据库
> - 忘记 commit 数据不会持久化！

---

### 4.2 查询（Read）

#### 4.2.1 查询所有

```python
# all(): 返回所有符合条件的记录，列表形式
all_stu = db.query(Student).all()

for stu in all_stu:
    print(stu.name, stu.age, stu.gender, stu.score)
```

#### 4.2.2 条件查询（filter）

```python
# filter(): 添加 WHERE 条件
# 成绩 >= 80 的学生
good_stu = db.query(Student).filter(Student.score >= 80).all()
```

#### 4.2.3 查询单条（first / get）

```python
# first(): 返回第一条匹配记录，不存在则返回 None
stu1 = db.query(Student).filter(Student.name == '张三').first()

# get(): 根据主键查询（仅支持主键）
stu2 = db.query(Student).get(1)   # 查询 id=1 的学生
```

#### 4.2.4 多条件查询（and_ / or_）

```python
from sqlalchemy import or_, and_

# AND 条件：年龄 > 18 且 成绩 >= 80
res = db.query(Student).filter(
    and_(Student.age > 18, Student.score >= 80)
).all()

# OR 条件：叫张三 或者 成绩 >= 90
res = db.query(Student).filter(
    or_(Student.name == '张三', Student.score >= 90)
).all()

# 链式 filter 等价于 AND
res = db.query(Student).filter(Student.age > 18).filter(Student.score >= 80).all()
```

#### 4.2.5 统计记录数（count）

```python
# count(): 直接返回查询结果的记录数
count = db.query(Student).count()
print(count)      # 10

# 条件统计
count = db.query(Student).filter(Student.score >= 80).count()
print(count)      # 5

# 注意：count() 和 func.count() + scalar() 的区别
# count()      → db.query().count()        返回 int
# func.count() → db.query(func.count()).scalar() 同样返回 int，但更灵活
```

---

### 4.3 修改（Update）

```python
# 1. 先查询要修改的对象
stu1 = db.query(Student).filter(Student.name == '张三').first()

# 2. 直接修改属性
stu1.score = 95.0
stu1.gender = '女'

# 3. 提交事务
db.commit()
print("修改成功")
```

> **原理：** SQLAlchemy 会跟踪被查询出的对象的属性变化，commit 时自动生成 UPDATE SQL。

---

### 4.4 删除（Delete）

```python
# 1. 查询要删除的对象
stu2 = db.query(Student).filter(Student.name == '李四').first()

# 2. 调用 delete 方法
db.delete(stu2)

# 3. 提交事务
db.commit()
print("删除成功")
```

---

### 4.5 完整 CRUD 示例

```python
# ========== 新增 ==========
stu = Student(name='赵六', age=22, gender='男', score=88.0)
db.add(stu)
db.commit()

# ========== 查询 ==========
all_stu = db.query(Student).all()
for s in all_stu:
    print(f"{s.name} - {s.score}分")

# ========== 修改 ==========
stu = db.query(Student).filter(Student.name == '赵六').first()
stu.score = 92.0
db.commit()

# ========== 删除 ==========
stu = db.query(Student).filter(Student.name == '赵六').first()
db.delete(stu)
db.commit()
```

---

## 5. 高级查询：排序、分页、模糊查询

### 5.1 排序（order_by）

```python
# 升序排序（默认）
sort_stu = db.query(Student).order_by(Student.score).all()

# 降序排序：字段名前加负号 -
sort_stu = db.query(Student).order_by(-Student.score).all()

for stu in sort_stu:
    print(stu.name, stu.score)   # 成绩从高到低
```

### 5.2 分页查询（offset + limit）

```python
# offset(n): 跳过前 n 条数据
# limit(m):  只取 m 条数据

# 第 1 页：取前 2 条
page1 = db.query(Student).offset(0).limit(2).all()

# 第 2 页：跳过 2 条，再取 2 条
page2 = db.query(Student).offset(2).limit(2).all()

# 第 3 页
page3 = db.query(Student).offset(4).limit(2).all()
```

> **分页公式：** `offset((page - 1) * page_size).limit(page_size)`

### 5.3 模糊查询（like）

```python
# % 是通配符，代表任意字符
# 查询名字中包含"王"的学生
res = db.query(Student).filter(Student.name.like('%王%')).all()

# 查询以"张"开头的学生
res = db.query(Student).filter(Student.name.like('张%')).all()

# 查询班级名中包含"班"的班级
res = db.query(Class).filter(Class.class_name.like('%班%')).all()
```

> **SQL 对照：**
> - `like('%王%')` → `WHERE name LIKE '%王%'`
> - `like('张%')` → `WHERE name LIKE '张%'`

---

## 6. 聚合统计（func 函数）

### 6.1 func 聚合函数

```python
from sqlalchemy import func
# func 提供了常见的 SQL 聚合函数：
#   COUNT, SUM, AVG, MAX, MIN, 等

# ========== 计数 COUNT ==========
total = db.query(func.count(Student.id)).scalar()
# scalar(): 返回单个标量值（而非列表或元组）

# ========== 平均值 AVG ==========
avg_score = db.query(func.avg(Student.score)).scalar()

# ========== 最大值 MAX ==========
max_score = db.query(func.max(Student.score)).scalar()

# ========== 最小值 MIN ==========
min_score = db.query(func.min(Student.score)).scalar()

# ========== 求和 SUM ==========
sum_score = db.query(func.sum(Student.score)).scalar()

# ========== 打印结果 ==========
print(f"总人数：{total}")
print(f"平均成绩：{avg_score:.2f}")
print(f"最高分：{max_score}")
print(f"最低分：{min_score}")
```

### 6.2 scalar() vs all()

```python
# scalar(): 返回单个值
count = db.query(func.count(Student.id)).scalar()
print(count)          # 10
print(type(count))    # <class 'int'>

# all(): 返回列表
result = db.query(func.count(Student.id)).all()
print(result)         # [(10,)]
print(type(result))   # <class 'list'>
```

---

## 7. 事务管理与异常回滚

### 7.1 什么是事务？

事务是一组要么全部成功、要么全部失败的操作。通过 `commit()` 确认，通过 `rollback()` 撤销。

### 7.2 基本事务回滚

```python
try:
    # 新增一条数据
    stu = Student(name='测试', age=18, gender='男', score=70.0)
    db.add(stu)

    # 模拟异常（如网络中断、逻辑错误等）
    1 / 0

    # 这行不会执行（因为上面抛异常了）
    db.commit()
    print("操作成功")

except Exception as e:
    # 出现任何异常，回滚撤销所有未提交的操作
    db.rollback()
    print(f"操作失败，已回滚：{e}")
    # 数据库不会被写入任何新数据
```

### 7.3 封装安全事务执行器

```python
def safe_execute(operations):
    """
    安全的批量操作执行器

    参数:
        operations: 函数列表，每个函数是一个数据库操作

    示例:
        safe_execute([
            lambda: db.add(Student(name='A', age=18, score=90)),
            lambda: setattr(db.query(Student).filter(Student.name=='B').first(), 'score', 95),
        ])
    """
    try:
        for op in operations:
            op()                           # 依次执行每个操作
        db.commit()                        # 全部成功才提交
        print("操作成功")

    except Exception as e:
        db.rollback()                      # 任一失败则全部回滚
        print(f"操作失败，已回滚：{e}")


# ========== 使用示例 ==========
safe_execute([
    lambda: db.add(Class(class_name='4班', teacher='王老师', student_num=30)),
    lambda: setattr(
        db.query(Class).filter(Class.class_name == '1班').first(),
        'teacher', '刘老师'
    ),
])
```

> **事务的核心原则（ACID）：**
>
> - **原子性 (Atomicity)**：要么全做，要么全不做
> - **一致性 (Consistency)**：操作前后数据库保持一致
> - **隔离性 (Isolation)**：并发事务互不影响
> - **持久性 (Durability)**：提交后的数据永久保存

---

## 8. 异步 SQLAlchemy（aiomysql）

### 8.1 为什么需要异步？

在 Web 开发中，数据库 IO 是常见的性能瓶颈。同步模式下，每次查询都会阻塞整个线程；异步模式下，可以在等待数据库响应时处理其他请求，大幅提升吞吐量。

```
同步：请求1 → [等待DB响应] → 请求2 → [等待DB响应] → 请求3
异步：请求1 → 请求2 → 请求3 → [并发等待]
```

### 8.2 安装 aiomysql

```bash
pip install aiomysql
```

### 8.3 异步引擎创建

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, select
from datetime import datetime
import asyncio

# ============ 异步引擎 ============
# 关键变化：
#   1. 使用 create_async_engine（不是 create_engine）
#   2. 连接字符串改成 mysql+aiomysql://
#   3. 会话工厂需要指定 class_=AsyncSession
engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4",
    echo=False
)

# class_=AsyncSession: 告诉 sessionmaker 创建异步会话而非普通会话
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
```

### 8.4 定义模型（与同步版完全相同）

```python
class JobPost(Base):
    """岗位表模型"""
    __tablename__ = "job_post"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    title = Column(String(100), nullable=False, comment="职位名称")
    company = Column(String(100), nullable=False, comment="公司名称")
    salary_min = Column(Float, default=0, comment="最低薪资(k)")
    salary_max = Column(Float, default=0, comment="最高薪资(k)")
    experience = Column(String(50), default="不限", comment="经验要求")
    jd_text = Column(Text, comment="职位描述原文")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<JobPost({self.title})@{self.company}>"
```

### 8.5 异步操作函数

#### 异步建表

```python
async def init_db():
    """异步创建所有表"""
    async with engine.begin() as conn:
        # run_sync: 在异步上下文中执行同步的 create_all
        await conn.run_sync(Base.metadata.create_all)
        print("数据表创建成功！")
```

#### 异步插入数据

```python
async def insert_job(title, company, salary_min, salary_max, experience, jd_text):
    """异步插入单条岗位数据"""
    async with AsyncSessionLocal() as db:
        job = JobPost(
            title=title,
            company=company,
            salary_min=salary_min,
            salary_max=salary_max,
            experience=experience,
            jd_text=jd_text
        )
        db.add(job)
        await db.commit()           # 异步提交
        await db.refresh(job)        # 刷新获取自增id
        print(f"插入成功：{job.title}，ID:{job.id}")
        return job.id
```

#### 异步查询数据

```python
async def query_jobs():
    """异步查询所有岗位"""
    async with AsyncSessionLocal() as db:
        # SQLAlchemy 2.0 风格：用 select() 而非 db.query()
        result = await db.execute(select(JobPost))
        jobs = result.scalars().all()
        print(f"共{len(jobs)}条数据")
        for job in jobs:
            print(job)
        return jobs
```

### 8.6 异步并发 vs 异步串行

```python
import random

# ============ 异步并发插入（快） ============
async def generate_jobs(count=500):
    """
    使用 asyncio.gather 实现并发插入
    所有请求几乎同时发出，效率极高
    """
    start = datetime.now()
    tasks = []                             # 收集所有协程任务
    for i in range(count):
        idx = random.randint(0, 19)
        tasks.append(insert_job(
            title=titles[idx],
            company=random.choice(companies),
            salary_min=random.randint(10, 30),
            salary_max=random.randint(15, 40),
            experience=random.choice(experiences),
            jd_text=job_desc[idx]
        ))
    await asyncio.gather(*tasks)           # 并发执行所有任务
    end = datetime.now()
    print(f"异步并发插入{count}条数据耗时：{end-start}")


# ============ 异步串行插入（慢，用于对比） ============
async def insert_jobs(count=500):
    """
    逐个 await，实际是串行执行
    仅用于对比演示，生产环境应使用并发版本
    """
    start = datetime.now()
    for i in range(count):
        idx = random.randint(0, 19)
        await insert_job(                  # 等待上一条完成才执行下一条
            title=titles[idx],
            company=random.choice(companies),
            salary_min=random.randint(10, 30),
            salary_max=random.randint(15, 40),
            experience=random.choice(experiences),
            jd_text=job_desc[idx]
        )
    end = datetime.now()
    print(f"异步串行插入{count}条数据耗时：{end-start}")
```

### 8.7 异步主函数

```python
async def main():
    # 1. 建表
    await init_db()

    # 2. 查询数据
    print("\n查询所有岗位数据==========")
    await query_jobs()

    # 3. 异步并发 vs 异步串行性能对比
    await generate_jobs(1000)     # 并发：快
    await insert_jobs(1000)       # 串行：慢

    # 4. 关闭引擎连接（必须在 await 之后，否则 Event loop is closed）
    await engine.dispose()
    print("数据库引擎已关闭")


if __name__ == "__main__":
    # Python 3.7+ 推荐用法
    asyncio.run(main())
```

> **异步 vs 同步关键区别：**
>
> | 方面 | 同步 | 异步 |
> |------|------|------|
> | 引擎函数 | `create_engine` | `create_async_engine` |
> | 连接字符串 | `mysql+pymysql://` | `mysql+aiomysql://` |
> | 会话类 | 默认 `Session` | `AsyncSession`（需指定 `class_=`） |
> | 函数定义 | `def func()` | `async def func()` |
> | 执行操作 | `db.execute()` | `await db.execute()` |
> | 提交 | `db.commit()` | `await db.commit()` |
> | 并发 | 不支持 | `asyncio.gather()` |
> | 入口 | 直接调用 | `asyncio.run(main())` |

---

## 9. 封装工具类实战

将全部 CRUD 操作封装为一个 **Tool 类**，方便复用：

```python
class Tool:
    """学生班级管理工具类"""

    def __init__(self):
        pass

    # ==================== 批量新增 ====================
    def insert_sc(self, student_list=[], class_list=[]):
        """批量新增学生和班级数据"""
        if student_list == [] and class_list == []:
            print("传入数据为空")
            return

        # 批量插入学生
        for stu in student_list:
            student = Student(
                name=stu.name, age=stu.age,
                gender=stu.gender, score=stu.score
            )
            db.add(student)
        db.commit()

        # 批量插入班级
        for cls in class_list:
            clas = Class(
                class_name=cls.class_name, teacher=cls.teacher,
                student_num=cls.student_num
            )
            db.add(clas)
        db.commit()

    # ==================== 排序 ====================
    def sort_cls(self):
        """班级按人数倒序排列"""
        sort_cls = db.query(Class).order_by(-Class.student_num).all()
        for cls in sort_cls:
            print(cls.class_name, cls.teacher, cls.student_num)

    def sort_stu(self):
        """学生按成绩倒序排列"""
        sort_stu = db.query(Student).order_by(-Student.score).all()
        for stu in sort_stu:
            print(stu.name, stu.age, stu.gender, stu.score)

    # ==================== 分页 ====================
    def page_stu(self, offset_, limit_):
        """学生分页查询"""
        page_stu = db.query(Student).offset(offset_).limit(limit_).all()
        for stu in page_stu:
            print(stu.name, stu.age, stu.gender, stu.score)

    def page_class(self, offset_, limit_):
        """班级分页查询"""
        page_cls = db.query(Class).offset(offset_).limit(limit_).all()
        for cls in page_cls:
            print(cls.class_name, cls.teacher, cls.student_num)

    # ==================== 条件查询 ====================
    def search_stu(self, name=None, min_score=None, max_score=None):
        """
        学生多条件组合查询
        - name: 按姓名模糊匹配
        - min_score: 最低分
        - max_score: 最高分
        """
        query = db.query(Student)       # 构建基础查询
        if name:
            query = query.filter(Student.name.like(f"%{name}%"))
        if min_score is not None:
            query = query.filter(Student.score >= min_score)
        if max_score is not None:
            query = query.filter(Student.score <= max_score)
        result = query.all()
        for stu in result:
            print(stu.name, stu.age, stu.gender, stu.score)

    def search_cls(self, name=None, teacher=None, min_num=None):
        """班级多条件组合查询"""
        query = db.query(Class)
        if name:
            query = query.filter(Class.class_name.like(f"%{name}%"))
        if teacher:
            query = query.filter(Class.teacher == teacher)
        if min_num is not None:
            query = query.filter(Class.student_num >= min_num)
        result = query.all()
        for cls in result:
            print(cls.class_name, cls.teacher, cls.student_num)

    # ==================== 事务回滚 ====================
    def safe_execute(self, operations):
        """
        安全批量操作，异常自动回滚
        operations: 函数列表，每个函数是一个数据库操作
        """
        try:
            for op in operations:
                op()
            db.commit()
            print("操作成功")
        except Exception as e:
            db.rollback()
            print(f"操作失败，已回滚：{e}")

    # ==================== 修改 ====================
    def update_stu(self, name, **kwargs):
        """
        按姓名修改学生信息
        例：update_stu('张三', score=95, gender='女')
        """
        stu = db.query(Student).filter(Student.name == name).first()
        if stu:
            for key, value in kwargs.items():
                setattr(stu, key, value)    # 动态设置属性
            db.commit()
            print(f"修改学生{name}成功")
        else:
            print(f"未找到学生{name}")

    def update_cls(self, class_name, **kwargs):
        """按班级名修改班级信息"""
        cls = db.query(Class).filter(Class.class_name == class_name).first()
        if cls:
            for key, value in kwargs.items():
                setattr(cls, key, value)
            db.commit()
            print(f"修改班级{class_name}成功")
        else:
            print(f"未找到班级{class_name}")

    # ==================== 删除 ====================
    def delete_stu(self, name):
        """按姓名删除学生"""
        stu = db.query(Student).filter(Student.name == name).first()
        if stu:
            db.delete(stu)
            db.commit()
            print(f"删除学生{name}成功")
        else:
            print(f"未找到学生{name}")

    def delete_cls(self, class_name):
        """按班级名删除班级"""
        cls = db.query(Class).filter(Class.class_name == class_name).first()
        if cls:
            db.delete(cls)
            db.commit()
            print(f"删除班级{class_name}成功")
        else:
            print(f"未找到班级{class_name}")

    # ==================== 数据统计 ====================
    def avg_num(self):
        """统计班级和学生数据"""
        print("班级聚合统计")
        total = db.query(func.count(Class.id)).scalar()
        avg_student_num = db.query(func.avg(Class.student_num)).scalar()
        print(f"总班级数：{total}")
        print(f"平均班级人数：{avg_student_num:.2f}")

        print("学生聚合统计")
        total = db.query(func.count(Student.id)).scalar()
        avg_score = db.query(func.avg(Student.score)).scalar()
        print(f"总人数：{total}")
        print(f"平均成绩：{avg_score:.2f}")
```

---

## 10. 同步 vs 异步性能对比实战

### 10.1 为什么需要做性能对比？

在真实项目中，选择同步还是异步方案需要数据支撑。本节通过一个完整的对比实验，量化同步/异步在批量插入场景下的性能差异。

### 10.2 核心思路

- **同步**：单线程逐条插入，每次 IO 阻塞线程
- **异步**：事件循环 + 协程，IO 等待期间可调度其他任务
- **测量指标**：相同数据量下的总耗时（秒）

### 10.3 完整实验代码

```python
"""
同步 vs 异步性能对比
演示：批量插入 500 条数据，对比同步和异步的耗时差异
"""
import asyncio
import time

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ========== 同步引擎 ==========
# 驱动用 pymysql
sync_engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/job_db?charset=utf8mb4",
    echo=False
)
SyncSession = sessionmaker(sync_engine)

# ========== 异步引擎 ==========
# 驱动用 aiomysql
async_engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost:3306/job_db?charset=utf8mb4",
    echo=False
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# ========== 模型定义 ==========
class PerfJob(Base):
    __tablename__ = "perf_job"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    salary_min = Column(Float, default=0)
    salary_max = Column(Float, default=0)
    experience = Column(String(50), default="不限")
    jd_text = Column(Text)

# ========== 生成测试数据 ==========
def generate_jobs(count=500):
    """批量生成模拟岗位数据"""
    companies = ["字节", "阿里", "腾讯", "美团", "京东", "百度", "网易", "快手"]
    titles = ["Python开发", "Java开发", "前端开发", "算法工程师", "测试开发"]
    experiences = ["1-3年", "3-5年", "5年以上", "不限"]

    jobs = []
    for i in range(count):
        jobs.append(PerfJob(
            title=f"{titles[i % len(titles)]}-{i}",
            company=f"{companies[i % len(companies)]}-部门{i}",
            salary_min=10 + (i % 25),
            salary_max=20 + (i % 30),
            experience=experiences[i % len(experiences)],
            jd_text=f"岗位{i}：负责相关开发工作..."
        ))
    return jobs

# ========== 同步批量插入 ==========
def sync_batch_insert(jobs):
    """同步批量插入：一次性 add_all + commit"""
    start = time.time()
    with SyncSession() as db:
        db.add_all(jobs)       # 批量添加到会话
        db.commit()            # 一次性提交
    elapsed = time.time() - start
    print(f"[同步] 插入 {len(jobs)} 条数据耗时: {elapsed:.3f} 秒")
    return elapsed

# ========== 异步批量插入 ==========
async def async_batch_insert(jobs):
    """异步批量插入：同样是一次性 add_all + await commit"""
    start = time.time()
    async with AsyncSessionLocal() as db:
        db.add_all(jobs)
        await db.commit()       # 异步提交
    elapsed = time.time() - start
    print(f"[异步] 插入 {len(jobs)} 条数据耗时: {elapsed:.3f} 秒")
    return elapsed

# ========== 主函数 ==========
async def main():
    print("=" * 50)
    print("同步 vs 异步 批量插入性能对比")
    print("=" * 50)

    # 生成测试数据（两份独立数据，防止缓存干扰）
    sync_jobs = generate_jobs(500)
    async_jobs = generate_jobs(500)

    # 同步测试
    sync_time = sync_batch_insert(sync_jobs)

    # 异步测试
    async_time = await async_batch_insert(async_jobs)

    # 打印对比结果
    print("\n" + "=" * 50)
    print("性能对比结果")
    print("=" * 50)
    print(f"同步耗时: {sync_time:.3f} 秒")
    print(f"异步耗时: {async_time:.3f} 秒")
    if async_time > 0:
        print(f"速度比: {sync_time/async_time:.2f}x")
    print("=" * 50)

    if sync_time > async_time:
        print("异步性能更优，在I/O密集场景下能更好地利用CPU")
    else:
        print("当前数据量较小或网络延迟低，差异不明显")
        print("在更大并发量、更高网络延迟场景下异步优势会更显著")

    # 关闭连接
    sync_engine.dispose()
    await async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
```

### 10.4 关键分析点

| 对比维度 | 同步 (pymysql) | 异步 (aiomysql) |
|----------|----------------|-----------------|
| 驱动 | `pymysql` | `aiomysql` |
| 引擎 | `create_engine` | `create_async_engine` |
| 提交 | `db.commit()` | `await db.commit()` |
| 关闭 | `engine.dispose()` | `await engine.dispose()` |
| 并发模型 | 单线程阻塞 | 事件循环 + 协程 |

> **实验结果解释：**
>
> - 在 500 条量级下，同步和异步差异可能不大（因为 `add_all` 本身已是批量操作）
> - 真正拉开差距的场景：**数百个并发请求**、**高网络延迟**、**大量独立查询**
> - 异步的核心优势不是"更快"，而是"能同时处理更多请求不阻塞"

---

## 11. 异步 CRUD 完整工具类封装

### 11.1 AsyncJobManager 工具类

将异步的增删改查、分页查询、条件过滤封装为一个可复用的工具类：

```python
import asyncio
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, select, func, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ========== 模型定义 ==========
Base = declarative_base()

class JobPost(Base):
    __tablename__ = "job_post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    salary_min = Column(Float, default=0)
    salary_max = Column(Float, default=0)
    experience = Column(String(50), default="不限")
    jd_text = Column(Text)
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<{self.title} @ {self.company} {self.salary_min}-{self.salary_max}k>"

    def to_dict(self):
        """
        将 ORM 对象转换为字典，方便 JSON 序列化
        这是异步开发中的常用模式，因为异步结果需要在不同协程间传递
        """
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "experience": self.experience,
            "create_time": str(self.create_time) if self.create_time else None
        }


# ========== 异步工具类 ==========
class AsyncJobManager:
    """异步岗位管理工具类"""

    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self):
        """初始化数据表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("数据表初始化完成")

    # ==================== 新增 ====================
    async def add_job(self, title: str, company: str, salary_min: float,
                      salary_max: float, experience: str, jd_text: str) -> int:
        """添加单条岗位，返回自增id"""
        async with self.async_session() as db:
            job = JobPost(
                title=title, company=company,
                salary_min=salary_min, salary_max=salary_max,
                experience=experience, jd_text=jd_text
            )
            db.add(job)
            await db.commit()
            await db.refresh(job)      # 刷新后才会有自增id
            print(f"添加成功: {job.title}")
            return job.id

    async def batch_add(self, jobs_data: List[Dict]) -> int:
        """
        批量添加岗位
        **kwargs 解包：JobPost(**data) 将字典展开为关键字参数
        例：{"title":"Python","company":"字节"} → JobPost(title="Python", company="字节")
        """
        async with self.async_session() as db:
            jobs = [JobPost(**data) for data in jobs_data]
            db.add_all(jobs)
            await db.commit()
            print(f"批量添加成功: {len(jobs)} 条")
            return len(jobs)

    # ==================== 查询 ====================
    async def query(self, salary_min: Optional[float] = None,
                    experience: Optional[str] = None) -> List[Dict]:
        """
        条件查询：按最低薪资、经验要求过滤
        SQLAlchemy 2.0 风格：select(JobPost).where(...)
        """
        async with self.async_session() as db:
            query = select(JobPost)
            if salary_min is not None:
                query = query.where(JobPost.salary_min >= salary_min)
            if experience is not None:
                query = query.where(JobPost.experience == experience)

            result = await db.execute(query)
            jobs = result.scalars().all()       # scalars() 提取 ORM 对象
            return [job.to_dict() for job in jobs]  # 统一转字典返回

    # ==================== 分页查询 ====================
    async def query_page(self, page: int = 1, page_size: int = 10,
                         salary_min: Optional[float] = None) -> Dict:
        """
        分页查询，返回 {total, page, page_size, data}
        分页公式：offset = (page - 1) * page_size
        """
        async with self.async_session() as db:
            query = select(JobPost)
            if salary_min is not None:
                query = query.where(JobPost.salary_min >= salary_min)

            # 先查总数（使用子查询避免两次全表扫描）
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await db.execute(count_query)
            total = total_result.scalar()

            # 再查分页数据
            query = query.limit(page_size).offset((page - 1) * page_size)
            result = await db.execute(query)
            jobs = result.scalars().all()

            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "data": [job.to_dict() for job in jobs]
            }

    # ==================== 更新 ====================
    async def update_job(self, job_id: int, **kwargs) -> bool:
        """
        按 ID 更新岗位，支持动态字段更新
        例：update_job(1, salary_min=25, salary_max=50)
        """
        async with self.async_session() as db:
            result = await db.execute(
                select(JobPost).where(JobPost.id == job_id)
            )
            job = result.scalars().first()
            if job:
                for key, value in kwargs.items():
                    if hasattr(job, key):          # 检查对象是否有该属性
                        setattr(job, key, value)   # 动态设置属性
                await db.commit()
                await db.refresh(job)
                print(f"更新成功: {job.title}")
                return True
            return False

    # ==================== 删除 ====================
    async def delete_job(self, job_id: int) -> bool:
        """按 ID 删除岗位"""
        async with self.async_session() as db:
            result = await db.execute(
                select(JobPost).where(JobPost.id == job_id)
            )
            job = result.scalars().first()
            if job:
                await db.delete(job)
                await db.commit()
                print(f"删除成功: {job.title}")
                return True
            return False

    async def close(self):
        """关闭引擎连接"""
        await self.engine.dispose()


# ========== 使用示例 ==========
async def main():
    manager = AsyncJobManager(
        "mysql+aiomysql://root:123456@localhost:3306/job_db?charset=utf8mb4"
    )
    await manager.init_db()

    # 1. 批量添加
    jobs_data = [
        {"title": "Python后端开发", "company": "字节跳动", "salary_min": 18,
         "salary_max": 35, "experience": "3-5年", "jd_text": "负责后端服务开发..."},
        {"title": "Java架构师", "company": "阿里巴巴", "salary_min": 30,
         "salary_max": 60, "experience": "5年以上", "jd_text": "负责核心系统架构..."},
        {"title": "前端工程师", "company": "腾讯", "salary_min": 15,
         "salary_max": 30, "experience": "1-3年", "jd_text": "负责Web端产品开发..."},
    ]
    await manager.batch_add(jobs_data)

    # 2. 条件查询：薪资 >= 20k
    results = await manager.query(salary_min=20)
    print(f"薪资>=20k的岗位: {len(results)} 条")

    # 3. 分页查询
    page_result = await manager.query_page(page=1, page_size=2)
    print(f"第1页: 总数={page_result['total']}, 本页={len(page_result['data'])}条")

    # 4. 更新
    if results:
        await manager.update_job(results[0]['id'], salary_min=25, salary_max=45)

    # 5. 删除
    if results:
        await manager.delete_job(results[-1]['id'])

    await manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 11.2 to_dict() 模式详解

```python
def to_dict(self):
    """
    将 ORM 对象转为字典
    为什么需要？
    1. ORM 对象不能直接 JSON 序列化（datetime 等类型）
    2. 异步场景下数据需要在协程间传递，字典是通用数据格式
    3. 避免"session已关闭后访问属性"的经典报错
    """
    return {
        "id": self.id,
        "title": self.title,
        "company": self.company,
        # datetime 需要手动转字符串
        "create_time": str(self.create_time) if self.create_time else None
    }
```

### 11.3 SQLAlchemy 2.0 select() 风格 vs 旧版 query() 风格

```python
# ===== 旧版 query() 风格（1.x，仍可用但官方建议迁移） =====
# db = Session()
# result = db.query(JobPost).filter(JobPost.salary_min >= 20).all()

# ===== 新版 select() 风格（2.0 推荐） =====
from sqlalchemy import select

async with AsyncSessionLocal() as db:
    # 构建查询
    stmt = select(JobPost).where(JobPost.salary_min >= 20)
    # 执行
    result = await db.execute(stmt)
    # 提取 ORM 对象
    jobs = result.scalars().all()
```

| 对比 | 旧版 query() | 新版 select() |
|------|-------------|--------------|
| 导入 | `db.query(Model)` | `from sqlalchemy import select` |
| 过滤 | `.filter()` | `.where()` |
| 执行 | 直接 `.all()` | `await db.execute(stmt)` 然后 `.scalars().all()` |
| 适配 | 同步 Session | 异步 AsyncSession（必须用新版） |

---

## 12. 综合实战：学生信息管理系统

### 12.1 需求概述

整合所有知识点，构建一个完整的学生信息管理小工具，包含：

1. 数据表创建
2. 批量新增测试数据
3. 多条件查询 + 排序 + 模糊查询
4. 修改和删除数据
5. 聚合统计（平均分）
6. 事务异常回滚保护

### 12.2 完整代码

```python
# 对应模块：综合实战 — 学生信息管理系统小工具

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ==================== 1. 数据库连接 ====================
engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/student_db?charset=utf8mb4"
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# ==================== 2. 模型定义 ====================
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer, default=18)
    gender = Column(String(10), default="未知")
    score = Column(Float)
    create_time = Column(DateTime, default=datetime.now)

class ClassTable(Base):
    __tablename__ = "class_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(30), nullable=False, unique=True)
    teacher = Column(String(20))
    student_num = Column(Integer, default=0)

# ==================== 3. 创建表 ====================
Base.metadata.create_all(bind=engine)

# ==================== 4. 功能函数 ====================
def add_test_data():
    """批量新增测试数据（含事务回滚保护）"""
    try:
        # 新增班级
        c = ClassTable(class_name="Python一班", teacher="王老师", student_num=42)
        db.add(c)

        # 批量新增学生
        stu_list = [
            Student(name="张三", age=19, gender="男", score=95),
            Student(name="李四", age=18, gender="女", score=88),
            Student(name="张小明", age=20, gender="男", score=79)
        ]
        db.add_all(stu_list)
        db.commit()
        print("测试数据新增完成")

    except Exception as e:
        db.rollback()
        print(f"新增失败：{e}")


def query_all_data():
    """综合查询：排序 + 模糊查询 + 聚合统计"""
    try:
        # 高分学生排序（降序）
        top_stu = db.query(Student).order_by(-Student.score).all()
        print("\n按分数倒序的学生列表：")
        for s in top_stu:
            print(f"  {s.name} - {s.score}分")

        # 模糊查询：姓"张"的学生
        z_stu = db.query(Student).filter(Student.name.like("%张%")).all()
        print(f"\n姓张的学生数量：{len(z_stu)}")

        # 聚合统计：平均分
        avg = db.query(func.avg(Student.score)).scalar()
        if avg:
            print(f"学生平均分：{avg:.2f}")

    except Exception as e:
        print(f"查询失败：{e}")


def update_del_data():
    """修改与删除数据（含异常回滚）"""
    try:
        # 修改：将李四的分数改为 90
        stu = db.query(Student).filter(Student.name == "李四").first()
        if stu:
            stu.score = 90
            db.commit()
            print(f"\n已修改李四的分数为 90")

        # 删除：删除分数 < 80 的学生
        del_stu = db.query(Student).filter(Student.score < 80).first()
        if del_stu:
            db.delete(del_stu)
            db.commit()
            print(f"已删除分数低于80的学生：{del_stu.name}")

    except Exception as e:
        db.rollback()
        print(f"操作失败：{e}")


# ==================== 5. 执行 ====================
if __name__ == "__main__":
    print("启动综合实战测试...")
    add_test_data()      # 新增
    query_all_data()     # 查询
    update_del_data()    # 修改+删除
    db.close()
```

### 12.3 架构要点

```
┌──────────────────────────────────────┐
│              主程序入口               │
├──────────────────────────────────────┤
│  add_test_data()    → 新增 + 回滚     │
│  query_all_data()   → 排序 + 模糊 + 统计 │
│  update_del_data()  → 修改 + 删除 + 回滚 │
├──────────────────────────────────────┤
│  db = SessionLocal()  → 全局会话      │
│  Base.metadata.create_all() → 自动建表 │
├──────────────────────────────────────┤
│  Student / ClassTable → ORM 模型      │
└──────────────────────────────────────┘
```

> **设计原则：**
>
> 1. **每个功能函数内部都有 try/except + rollback**，保证单个操作异常不影响其他操作
> 2. **先查后改**：修改和删除前先 `first()` 判断是否存在
> 3. **批量操作用 `add_all`**，减少与数据库的交互次数
> 4. **聚合统计用 `scalar()`**，返回纯数值而非元组

---

## 13. 知识点速查表

### 13.1 SQLAlchemy 核心 API

| API | 说明 | 示例 |
|-----|------|------|
| `create_engine(url)` | 创建数据库引擎 | `create_engine('mysql+pymysql://...')` |
| `declarative_base()` | 创建 ORM 基类 | `Base = declarative_base()` |
| `sessionmaker(bind=engine)` | 创建会话工厂 | `SessionLoc = sessionmaker(...)` |
| `Base.metadata.create_all(engine)` | 自动建表 | 基于所有模型类创建表 |
| `db.add(obj)` | 新增记录 | `db.add(stu)` |
| `db.add_all([obj1, obj2])` | 批量新增 | `db.add_all([s1, s2])` |
| `db.commit()` | 提交事务 | 把修改写入数据库 |
| `db.rollback()` | 回滚事务 | 撤销未提交的修改 |
| `db.delete(obj)` | 删除记录 | `db.delete(stu)` |
| `db.query(Model)` | 构建查询 | `db.query(Student)` |
| `.filter(条件)` | WHERE 条件 | `.filter(Student.age > 18)` |
| `.all()` | 获取所有结果 | 返回 list |
| `.first()` | 获取第一条 | 返回对象或 None |
| `.order_by(字段)` | 排序（升序） | `.order_by(Student.score)` |
| `.order_by(-字段)` | 排序（降序） | `.order_by(-Student.score)` |
| `.offset(n)` | 跳过 n 条 | `.offset(5)` |
| `.limit(m)` | 取 m 条 | `.limit(10)` |
| `.like(pattern)` | 模糊匹配 | `.like('%张%')` |

### 13.2 func 聚合函数

| 函数 | SQL 等价 | 说明 |
|------|---------|------|
| `func.count(字段)` | `COUNT(*)` | 计数 |
| `func.sum(字段)` | `SUM()` | 求和 |
| `func.avg(字段)` | `AVG()` | 平均值 |
| `func.max(字段)` | `MAX()` | 最大值 |
| `func.min(字段)` | `MIN()` | 最小值 |

### 13.3 查询结果获取方法

| 方法 | 返回值 | 适用场景 |
|------|--------|---------|
| `.all()` | `list[Model]` | 多条记录 |
| `.first()` | `Model` 或 `None` | 单条记录 |
| `.scalar()` | 单个值 | 聚合查询结果 |
| `.scalars().all()` | `list[value]` | SQLAlchemy 2.0 select |

### 13.4 异步 SQLAlchemy API

| 同步 | 异步 | 说明 |
|------|------|------|
| `create_engine()` | `create_async_engine()` | 引擎创建 |
| `Session` | `AsyncSession` | 会话类 |
| `db.commit()` | `await db.commit()` | 提交 |
| `sessionmaker(bind=engine)` | `sessionmaker(engine, class_=AsyncSession)` | 会话工厂 |
| — | `await engine.dispose()` | 关闭引擎 |
| — | `await conn.run_sync(func)` | 在异步中执行同步函数 |
| — | `asyncio.gather(*tasks)` | 并发执行多个协程 |
| — | `asyncio.run(main())` | 运行异步主函数 |

### 13.5 PyMySQL 常用操作

| 方法/属性 | 说明 |
|-----------|------|
| `pymysql.connect(...)` | 建立数据库连接 |
| `conn.cursor()` | 创建游标 |
| `cursor.execute(sql, args)` | 执行 SQL |
| `cursor.fetchone()` | 获取一条记录 |
| `cursor.fetchall()` | 获取所有记录 |
| `conn.commit()` | 提交事务 |
| `cursor.rowcount` | 受影响行数（属性，非方法） |
| `cursor.close()` | 关闭游标 |
| `conn.close()` | 关闭连接 |

---

> **学习建议：**
>
> 1. 先用 PyMySQL 理解 SQL 底层 → 再用 SQLAlchemy ORM 提高开发效率
> 2. 掌握 CRUD 后重点练习条件查询和聚合统计
> 3. 事务回滚是生产环境必须掌握的技能
> 4. 异步版本适合高并发 Web 服务，理解了同步再学异步更容易
>
> **文件对应关系：**
>
> | 文件路径 | 对应知识点 |
> |----------|-----------|
> | `sql_tool.py` | PyMySQL 封装 |
> | `sqlalchemy_bind.py` | 引擎创建、连接、`text()` 原始 SQL |
> | `sqlalchemy_create.py` | 学生表模型定义、`create_all` 建表 |
> | `sqlalchemy_basemodel.py` | 班级表模型定义 |
> | `sqlalchemy_CRUD.py` | CRUD、排序、分页、聚合、事务回滚 |
> | `sqlalchemy_test.py` | Tool 同步工具类封装（完整版） |
> | `async1_异步引擎创建.py` | 异步 SQLAlchemy + 并发 vs 串行 |
> | `_0721_SQLAlchemy/alchemy1_连接数据库.py` | 引擎创建与连接测试 |
> | `_0721_SQLAlchemy/alchemy2_定义模型与建表.py` | Student + ClassTable 双模型、`.count()` |
> | `_0721_SQLAlchemy/alchemy3_增删改查回滚.py` | CRUD、`.get()` 主键查询、事务回滚 |
> | `_0721_SQLAlchemy/alchemy3_异步增删改查.py` | AsyncJobManager 工具类、`to_dict()` 模式 |
> | `_0721_SQLAlchemy/alchemy4_综合任务.py` | 学生信息管理系统综合实战 |
> | `_0721_SQLAlchemy/async1_异步引擎创建.py` | 异步引擎、异步建表、异步查询 |
> | `_0721_SQLAlchemy/async2_同步异步alchemy_performance_compare.py` | 同步 vs 异步性能对比实验 |
> | `_0721_SQLAlchemy/async3_crud异步sqlalchemy.py` | 异步 CRUD 完整工具类 + 分页 + 演示 |
