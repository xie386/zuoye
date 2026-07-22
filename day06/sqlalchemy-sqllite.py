from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base
#如果不存在test.db文件，会自动创建
engine = create_engine("sqlite:///test.db",echo=False)
Base = declarative_base()
Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    name = Column(String(20))
    email = Column(String(50))
    age = Column(Integer)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = Session()
    user = User(name="张三",email="zhangsan@example.com",age=30)
    db.add(user)
    db.commit()
    print("插入成功")
    db.close()