"""
3\. 学生实操任务（30min）

#### 任务要求

1. 复用数据库连接代码
  
2. 新建**班级表 Class**，表名 class\_table
  
3. 字段：id\(主键自增\)、class\_name\(班级名，非空唯一\)、
teacher\(班主任\)、student\_num\(人数，默认0\)
  
4. 运行代码自动创建数据表
"""
from sqlalchemy import create_engine,text,Column,Integer,String,Float,DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
engine=create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4',echo=True
    )
Base=declarative_base()
SessionLoc=sessionmaker(autoflush=False,autocommit=False,bind=engine)
db=SessionLoc()
class Class(Base):
    __tablename__='class_table'
    id=Column(Integer,primary_key=True,autoincrement=True,comment='主键')
    class_name=Column(String(20),nullable=False,unique=True,comment='班级名')
    teacher=Column(String(20),nullable=False,comment='班主任')
    student_num=Column(Integer,default=0,comment='人数')
    create_time=Column(DateTime,default=datetime.now,comment='创建时间')
#创建数据库表
Base.metadata.create_all(engine)
print("数据库表创建成功")
