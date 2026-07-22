"""
第1小时：同步 vs 异步性能对比
演示：批量插入 500 条数据，对比同步和异步的耗时差异
"""
import asyncio
import time
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ========== 同步引擎 ==========
sync_engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/job_db?charset=utf8mb4",
    echo=False
)
SyncSession = sessionmaker(sync_engine)

# ========== 异步引擎 ==========
async_engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost:3306/job_db?charset=utf8mb4",
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


# ========== 生成测试数据 ==========
def generate_jobs(count=500):
    """模拟 JD 数据"""
    companies = ["字节", "阿里", "腾讯", "美团", "京东", "百度", "网易", "快手"]
    titles = ["Python开发", "Java开发", "前端开发", "算法工程师", "测试开发", "运维工程师"]
    experiences = ["1-3年", "3-5年", "5年以上", "不限"]
    jd_templates = [
        "岗位{i}：需要掌握Python、MySQL、Redis等技术，有Web开发经验优先...",
        "岗位{i}：负责Java微服务开发，熟悉Spring Cloud、Docker、K8s...",
        "岗位{i}：负责前端产品迭代，精通Vue3/React、TypeScript...",
        "岗位{i}：负责推荐算法优化，熟悉机器学习、深度学习框架...",
    ]

    jobs = []
    for i in range(count):
        jobs.append(PerfJob(
            title=f"{titles[i % len(titles)]}-{i}",
            company=f"{companies[i % len(companies)]}-部门{i}",
            salary_min=10 + (i % 25),
            salary_max=20 + (i % 30),
            experience=experiences[i % len(experiences)],
            jd_text=jd_templates[i % len(jd_templates)].format(i=i)
        ))
    return jobs


# ========== 同步批量插入 ==========
def sync_batch_insert(jobs):
    """同步方式批量插入"""
    start = time.time()
    with SyncSession() as db:
        db.add_all(jobs)
        db.commit()
    elapsed = time.time() - start
    print(f"[同步] 插入 {len(jobs)} 条数据耗时: {elapsed:.3f} 秒")
    return elapsed


# ========== 异步批量插入 ==========
async def async_batch_insert(jobs):
    """异步方式批量插入"""
    start = time.time()
    async with AsyncSessionLocal() as db:
        db.add_all(jobs)
        await db.commit()
    elapsed = time.time() - start
    print(f"[异步] 插入 {len(jobs)} 条数据耗时: {elapsed:.3f} 秒")
    return elapsed


# ========== 异步建表 ==========
async def init_sync_db():
    with sync_engine.begin() as conn:
        from sqlalchemy import text
        conn.execute(text("DROP TABLE IF EXISTS perf_job"))
        conn.execute(text("CREATE TABLE perf_job ("
                         "id INT AUTO_INCREMENT PRIMARY KEY, "
                         "title VARCHAR(100) NOT NULL, "
                         "company VARCHAR(100) NOT NULL, "
                         "salary_min FLOAT DEFAULT 0, "
                         "salary_max FLOAT DEFAULT 0, "
                         "experience VARCHAR(50) DEFAULT '不限', "
                         "jd_text TEXT, "
                         "create_time DATETIME DEFAULT CURRENT_TIMESTAMP"
                         ")"))
    print("同步测试表创建成功")


async def init_async_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(PerfJob.metadata.create_all)
    print("异步测试表创建成功")


# ========== 主函数 ==========
async def main():
    print("=" * 50)
    print("同步 vs 异步 批量插入性能对比")
    print("=" * 50)

    # 初始化表
    await init_sync_db()
    await init_async_db()

    # 生成测试数据
    sync_jobs = generate_jobs(500)
    async_jobs = generate_jobs(500)

    print("\n--- 开始测试 ---")

    # 同步测试
    sync_time = sync_batch_insert(sync_jobs)

    # 异步测试
    async_time = await async_batch_insert(async_jobs)

    # 对比结果
    print("\n" + "=" * 50)
    print("性能对比结果")
    print("=" * 50)
    print(f"同步耗时: {sync_time:.3f} 秒")
    print(f"异步耗时: {async_time:.3f} 秒")
    if async_time > 0:
        print(f"速度比: {sync_time/async_time:.2f}x")
    print("=" * 50)

    # 分析
    print("\n分析:")
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
