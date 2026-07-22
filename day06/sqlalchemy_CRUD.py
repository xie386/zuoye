from sqlalchemy import create_engine,text,Column,Integer,String,Float,DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
from sqlalchemy import or_,and_
from sqlalchemy import func

engine=create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4',echo=False
    )
Base=declarative_base()
SessionLoc=sessionmaker(autoflush=False,autocommit=False,bind=engine)
db=SessionLoc()
class Student(Base):
    __tablename__='students'
    #autoincrement=True:自增主键
    id=Column(Integer,primary_key=True,autoincrement=True,comment='主键')
    name=Column(String(20),nullable=False,comment='姓名')
    age=Column(Integer,nullable=False,default=18,comment='年龄')
    gender=Column(String(10),default='未知',comment='性别')
    score=Column(Float,default=0.0,comment='成绩')
    create_time=Column(DateTime,default=datetime.now,comment='创建时间')
class Class(Base):
    __tablename__='class_table'
    id=Column(Integer,primary_key=True,autoincrement=True,comment='主键')
    class_name=Column(String(20),nullable=False,unique=True,comment='班级名')
    teacher=Column(String(20),nullable=False,comment='班主任')
    student_num=Column(Integer,default=0,comment='人数')
    create_time=Column(DateTime,default=datetime.now,comment='创建时间')

#======================CRUD操作========================================
"""
stu1=Student(name='张八',age=18,gender='男',score=70.0)
stu2=Student(name='李四',age=19,gender='女',score=85.0)
stu3=Student(name='王五',age=20,gender='男',score=95.0)
db.add(stu1)
db.add(stu2)
db.add(stu3)
all_stu=db.query(Student).all()
for stu in all_stu:
    print(stu.name,stu.age,stu.gender,stu.score)
good_stu=db.query(Student).filter(Student.score>=80).all()
for stu in good_stu:
    print(stu.name,stu.age,stu.gender,stu.score)
db.commit()
"""
"""
* 向班级表新增2条班级数据
  
* 查询**所有班级**、**主键为1的班级**、**人数大于0的班级**
  
* 遍历查询结果，打印班级名称和班主任

Class1=Class(class_name='1班',teacher='张老师',student_num=30)
Class2=Class(class_name='2班',teacher='李老师',student_num=25)
Class3=Class(class_name='3班',teacher='王老师',student_num=0)
db.add(Class1)
db.add(Class2)
db.add(Class3)
#必需要提交事务才能生效
db.commit()
all_class=db.query(Class).all()
#查询所有班级
print("所有班级：")
for cls in all_class:
    print(f"班级名称：{cls.class_name},班主任：{cls.teacher}")
#查询主键为1的班级
print("主键为1的班级：")
cls1=db.query(Class).filter(Class.id==1).first()
print(f"班级名称：{cls1.class_name},班主任：{cls1.teacher}")
#查询人数大于0的班级
print("人数大于0的班级：")
for cls in all_class:
    if cls.student_num>0:
        print(f"班级名称：{cls.class_name},班主任：{cls.teacher}")
        print(f"人数：{cls.student_num}")
db.commit()

"""


"""
修改和删除操作

stu1=db.query(Student).filter(Student.name=="张八").first()
stu1.score=80.0
db.commit()
print("修改成功")

stu2=db.query(Student).filter(Student.name=="李四").first()
db.delete(stu2)
db.commit()
print("删除成功")
"""

"""
异常事务回滚
try:
    stu=Student(name='张嘎',age=18,gender='男',score=70.0)
    1/0#模拟异常
    db.add(stu)
    db.commit()
    print("修改成功")
except Exception as e:
    db.rollback()
    print(f"修改失败：{e}")
"""


"""
实操训练:
任务要求

1. 修改二班的班主任为「张老师」，人数改为40
  
2. 删除任意一条班级数据
  
3. 编写事务代码：同时新增1个班级+修改1个班级，模拟异常回滚


cls2=db.query(Class).filter(Class.class_name=="2班").first()
cls2.teacher="张老师"
cls2.student_num=40
db.commit()
print("修改成功")
try:
    #同时新增1个班级+修改1个班级，模拟异常回滚
    cls5=Class(class_name='5班',teacher='赵老师',student_num=30)
    db.add(cls5)
    cls2=db.query(Class).filter(Class.class_name=="1班").first()
    cls2.teacher="刘老师"
    1/0  #模拟异常，触发回滚
    db.commit()
    print("操作成功")
except Exception as e:
    db.rollback()
    print(f"操作失败，已回滚：{e}")
"""
#排序和分页
print("排序：")
sort_stu=db.query(Student).order_by(-Student.score).all()
for stu in sort_stu:
    print(stu.name,stu.age,stu.gender,stu.score)
#分页
print("分页：")
page_stu=db.query(Student).offset(1).limit(2).all()
for stu in page_stu:
    print(stu.name,stu.age,stu.gender,stu.score)

#模糊查询
print("模糊查询：")
good_stu=db.query(Student).filter(Student.name.like("%王%")).all()
for stu in good_stu:
    print(stu.name,stu.age,stu.gender,stu.score)

#聚合统计
#func功能:统计行数、平均值、最大值、最小值、总和等
#scalar():返回单个值
print("聚合统计：")
total=db.query(func.count(Student.id)).scalar()
avg_score=db.query(func.avg(Student.score)).scalar()
print(f"总人数：{total}")
print(f"平均成绩：{avg_score:.2f}")


"""
* 对班级表按人数倒序排序
  
* 分页查询：第1页，每页1条数据
  
* 模糊查询班级名包含“班”的班级
  
* 统计班级总数量、总人数平均值
"""
#排序
print("排序：")
sort_cls=db.query(Class).order_by(-Class.student_num).all()
for cls in sort_cls:
    print(cls.class_name,cls.teacher,cls.student_num)
#分页
print("分页：")
#offset(1):跳过1条数据，从第2条数据开始查询
#limit(1):查询1条数据
page_cls=db.query(Class).offset(1).limit(1).all()
for cls in page_cls:
    print(cls.class_name,cls.teacher,cls.student_num)
#模糊查询
print("模糊查询：")
good_cls=db.query(Class).filter(Class.class_name.like("%班%")).all()
for cls in good_cls:
    print(cls.class_name,cls.teacher,cls.student_num)
#聚合统计
print("聚合统计：")
total=db.query(func.count(Class.id)).scalar()
avg_student_num=db.query(func.avg(Class.student_num)).scalar()
print(f"总班级数：{total}")
print(f"平均班级人数：{avg_student_num:.2f}")
