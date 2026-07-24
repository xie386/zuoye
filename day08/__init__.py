import os
from functools import wraps 
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'company.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Company_news(Base):
    __tablename__ = 'company_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    content = Column(Text)
    # 新闻分类
    category = Column(String(255))
    date = Column(DateTime, default=datetime.now)

class Company_user(Base):
    __tablename__ = 'company_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    role = Column(String(255))

Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass