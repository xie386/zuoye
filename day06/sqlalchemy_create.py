from sqlalchemy import create_engine,text,Column,Integer,String,Float,DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
engine=create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4',echo=True
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
#创建数据库表
Base.metadata.create_all(engine)
print("数据库表创建成功")