"""
1\. 实战需求（15min讲解）
完成**简易学生班级管理小工具**，实现全套功能：
1. 数据表模型创建（学生表\+班级表）
2. 批量新增测试数据
3. 条件查询、排序、分页查询
4. 修改、删除数据
5. 事务异常回滚保护
6. 数据统计（平均分、总人数）
"""

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

class Tool:
    def __init__(self):
        pass
    #2. 批量新增测试数据
    def insert_sc(self,student_list=[],class_list=[]):
        if student_list==[] and class_list==[]:
            print("传入数据为空")
            return
        for stu in student_list:
            student=Student(name=stu.name,age=stu.age,gender=stu.gender,score=stu.score)
            db.add(student)
        db.commit()

        for cls in class_list:
            clas=Class(class_name=cls.class_name,teacher=cls.teacher,student_num=cls.student_num)
            db.add(clas)
        db.commit()
    #3. 排序、分页查询
    def sort_cls(self):
        sort_cls=db.query(Class).order_by(-Class.student_num).all()
        for cls in sort_cls:
            print(cls.class_name,cls.teacher,cls.student_num)
    def sort_stu(self):
        sort_stu=db.query(Student).order_by(-Student.score).all()
        for stu in sort_stu:
            print(stu.name,stu.age,stu.gender,stu.score)
    def page_stu(self,offset_,limit_):
        page_stu=db.query(Student).offset(offset_).limit(limit_).all()
        for stu in page_stu:
            print(stu.name,stu.age,stu.gender,stu.score)
    def page_class(self,offset_,limit_):
        page_cls=db.query(Class).offset(offset_).limit(limit_).all()
        for cls in page_cls:
            print(cls.class_name,cls.teacher,cls.student_num)
    #条件查询
    def search_stu(self,name=None,min_score=None,max_score=None):
        query=db.query(Student)
        if name:
            query=query.filter(Student.name.like(f"%{name}%"))
        if min_score is not None:
            query=query.filter(Student.score>=min_score)
        if max_score is not None:
            query=query.filter(Student.score<=max_score)
        result=query.all()
        for stu in result:
            print(stu.name,stu.age,stu.gender,stu.score)
    def search_cls(self,name=None,teacher=None,min_num=None):
        query=db.query(Class)
        if name:
            query=query.filter(Class.class_name.like(f"%{name}%"))
        if teacher:
            query=query.filter(Class.teacher==teacher)
        if min_num is not None:
            query=query.filter(Class.student_num>=min_num)
        result=query.all()
        for cls in result:
            print(cls.class_name,cls.teacher,cls.student_num)

    #事务异常回滚保护
    def safe_execute(self,operations):
        try:
            for op in operations:
                op()
            db.commit()
            print("操作成功")
        except Exception as e:
            db.rollback()
            print(f"操作失败，已回滚：{e}")

    #修改数据
    def update_stu(self,name,**kwargs):
        stu=db.query(Student).filter(Student.name==name).first()
        if stu:
            for key,value in kwargs.items():
                setattr(stu,key,value)
            db.commit()
            print(f"修改学生{name}成功")
        else:
            print(f"未找到学生{name}")
    def update_cls(self,class_name,**kwargs):
        cls=db.query(Class).filter(Class.class_name==class_name).first()
        if cls:
            for key,value in kwargs.items():
                setattr(cls,key,value)
            db.commit()
            print(f"修改班级{class_name}成功")
        else:
            print(f"未找到班级{class_name}")

    #删除数据
    def delete_stu(self,name):
        stu=db.query(Student).filter(Student.name==name).first()
        if stu:
            db.delete(stu)
            db.commit()
            print(f"删除学生{name}成功")
        else:
            print(f"未找到学生{name}")
    def delete_cls(self,class_name):
        cls=db.query(Class).filter(Class.class_name==class_name).first()
        if cls:
            db.delete(cls)
            db.commit()
            print(f"删除班级{class_name}成功")
        else:
            print(f"未找到班级{class_name}")

    #数据统计（平均分、总人数）
    def avg_num(self):
        print("班级聚合统计")
        total=db.query(func.count(Class.id)).scalar()
        avg_student_num=db.query(func.avg(Class.student_num)).scalar()
        print(f"总班级数：{total}")
        print(f"平均班级人数：{avg_student_num:.2f}")
        print("学生聚合统计")
        total=db.query(func.count(Student.id)).scalar()
        avg_score=db.query(func.avg(Student.score)).scalar()
        print(f"总人数：{total}")
        print(f"平均成绩：{avg_score:.2f}")
