from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base

#创建数据库引擎
#格式:数据库驱动+数据库连接库://用户名:密码@主机:端口/数据库名
#?charset=utf8mb4:指定字符集为utf8mb4
engine=create_engine(
    'mysql+pymysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4',echo=True
    )
#创建模型基类
Base=declarative_base()
#会话工厂
#echo=True:打印SQL语句日志,方便调试
SessionLoc=sessionmaker(autoflush=False,autocommit=False,bind=engine)
db=SessionLoc()
result=db.execute(text('select * from student'))
print(result.fetchall())
print("数据库连接成功")
db.close()