from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
import asyncio
from sqlalchemy import select
import random
companies=[#20个无重复公司
        "字节跳动","阿里巴巴","腾讯","华为","美团","京东","百度","拼多多",
        "网易","小米","快手","滴滴","哔哩哔哩","携程","新浪","搜狐",
        "360","商汤科技","旷视科技","科大讯飞"
    ]
titles=[#20个无重复岗位名称
        "Python开发工程师","Java高级工程师","前端开发工程师","Go后端开发","C++开发工程师",
        "数据分析师","算法工程师","测试开发工程师","运维工程师","DevOps工程师",
        "Android开发工程师","iOS开发工程师","全栈开发工程师","大数据开发工程师","AI工程师",
        "安全工程师","产品经理","UI设计师","DBA数据库管理员","架构师"
    ]
experiences=[#20个无重复经验要求
        "应届生","1年以上","2年以上","3年以上","4年以上",
        "5年以上","6年以上","7年以上","8年以上","9年以上",
        "10年以上","1-3年","3-5年","5-10年","不限",
        "2-4年","4-6年","6-8年","8-10年","10年及以上"
    ]
job_desc=[#20个无重复岗位描述
        "负责核心业务系统的设计、开发与维护，参与技术方案评审",
        "参与高并发分布式系统的架构设计与核心模块开发",
        "负责数据平台的搭建，包括数据采集、清洗、存储和分析",
        "负责移动端App的功能开发与性能优化",
        "参与AI算法模型的训练、调优与部署上线",
        "负责自动化测试框架搭建，编写测试用例，保障产品质量",
        "负责服务器运维、监控、故障排查与性能调优",
        "参与CI/CD流水线搭建，推动研发效能提升",
        "负责用户增长策略的数据分析与AB实验设计",
        "参与微服务架构的拆分、治理与中间件选型",
        "负责安全漏洞扫描、渗透测试与安全加固",
        "参与技术中台建设，输出通用组件与最佳实践",
        "负责BI报表开发，为业务决策提供数据支撑",
        "参与低代码平台搭建，提升业务交付效率",
        "负责推荐系统的算法优化与效果评估",
        "参与云原生技术的落地，包括容器化、服务网格等",
        "负责数据库的日常管理、备份恢复与SQL优化",
        "参与技术难题攻关，输出技术方案与专利文档",
        "负责跨部门技术沟通，推动项目按时高质量交付",
        "参与开源社区贡献，跟踪前沿技术发展动态"
    ]
    
#1. 异步引擎创建
#注意：驱动从pymysql改成aiomysql，协议也用mysql+变成mysql+aiomysql
engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost:3306/ZQK4?charset=utf8mb4",
    echo=False
    )

# 异步会话工厂，需要指定class_=AsyncSession
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# 2.定义模型
class JobPost(Base):
    __tablename__ = "job_post"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    title = Column(String(100), nullable=False, comment="职位名称")
    company = Column(String(100), nullable=False, comment="公司名称")
    salary_min = Column(Float, default=0, comment="最低薪资(k)")
    salary_max = Column(Float, default=0, comment="最高薪资(k)")
    experience = Column(String(50), default="不限", comment="经验要求")
    jd_text = Column(Text, comment="职位描述原文")
    vector_id = Column(String(100), comment="关联向量ID")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<JobPost(self.titile)@{self.company}>"

# 3.异步建表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("数据表创建成功！")


# 4.异步插入数据
async def insert_job(title, company, salary_min, salary_max, experience, jd_text):
    # 插入单条岗位
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
        await db.commit()
        await db.refresh(job) #刷新获取自增id
        print(f"插入成功：{job.title}，ID:{job.id}")
        return job.id

# 5.异步查询数据
async def query_jobs():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(JobPost))
        jobs = result.scalars().all()
        print(f"共{len(jobs)}条数据")
        for job in jobs:
            print(job)
        return jobs
#批量随机异步并发插入岗位数据 
async def generate_jobs(count=500):#count:插入条数
    start=datetime.now()
    tasks=[]
    for i in range(count):
        idx=random.randint(0,19)
        tasks.append(insert_job(
            title=titles[idx],
            company=random.choice(companies),
            salary_min=random.randint(10, 30),
            salary_max=random.randint(15, 40),
            experience=random.choice(experiences),
            jd_text=job_desc[idx]
        ))
    await asyncio.gather(*tasks)
    end=datetime.now()
    print(f"异步并发插入{count}条数据耗时：{end-start}")
    return end-start

#批量随机异步串行插入岗位数据（对比异步并发）
async def insert_jobs(count=500):
    start=datetime.now()
    for i in range(count):
        idx=random.randint(0,19)
        await insert_job(
            title=titles[idx],
            company=random.choice(companies),
            salary_min=random.randint(10, 30),
            salary_max=random.randint(15, 40),
            experience=random.choice(experiences),
            jd_text=job_desc[idx]
        )
    end=datetime.now()
    print(f"异步串行插入{count}条数据耗时：{end-start}")
    return end-start
       #================主函数=================
async def main():
    #1. 建表
    await init_db()

    # #2. 插入示例数据
    # await insert_job(
    #     title="Python开发",
    #     company="字节跳动",
    #     salary_min=15,
    #     salary_max=20,
    #     experience="3年以上",
    #     jd_text="负责Python项目的开发，包括后端、前端、数据库等。"
    # )
    # await insert_job(
    #     "Java高级工程师", "阿里巴巴", 20, 40,
    #     "5年以上", "负责核心交易系统，精通Java、Spring Cloud、MySQL..."
    # )
    # await insert_job(
    #     "前端开发工程师", "腾讯", 12, 25,
    #     "1-3年", "负责Web端产品开发，熟悉Vue3、TypeScript..."
    # )
    # await insert_job(
    #     "算法工程师", "百度", 25, 50,
    #     "3-5年", "负责NLP算法研发，熟悉Transformer、BERT..."
    # )
    # await insert_job(
    #     "测试开发工程师", "美团", 10, 20,
    #     "不限", "负责自动化测试框架搭建，熟悉Python、Selenium..."
    # )
    #3. 查询数据
    print("\n查询所有岗位数据==========")
    await query_jobs()

    #4. 异步并发插入 vs 异步串行插入 性能对比
    time1=await generate_jobs(1000)
    time2=await insert_jobs(1000)
    print(f"异步并发插入耗时：{time1}")
    print(f"异步串行插入耗时：{time2}")

    #5. 关闭引擎连接 （避免Event loop is closed)
    await engine.dispose()
    print("数据库引擎已关闭")

if __name__ == "__main__":
    asyncio.run(main())




