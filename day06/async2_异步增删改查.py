import asyncio
from datetime import datetime
from typing import List, Dict,Any,Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Text,select,func
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
async_engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4",
    echo=False
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


class PerfJob(Base):
    __tablename__ = "perf_job"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    salary_min = Column(Float, default=0)
    salary_max = Column(Float, default=0)
    experience = Column(String(50), default="不限")
    jd_text = Column(Text)
    create_time = Column(DateTime, default=datetime.now)


class asyncJobManager:
    def __init__(self):
        self.engine = async_engine()
        self.async_session = AsyncSessionLocal()
    async def init_db(self):
        await self.async_session.run_sync(Base.metadata.create_all)
        await self.async_session.commit()
        print("数据库初始化完成")
