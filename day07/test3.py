import requests
import time
import random
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
"""
Python爬虫自学任务书：BeautifulSoup抓取政府网新闻 
一、任务信息 
1.  依托讲义：HTTP协议、requests、SQLAlchemy、XPath解析  
2.  技术栈：requests + BeautifulSoup4 + lxml + SQLite  
3.  目标网址：https://www.gov.cn/toutiao/liebiao/  
4.  核心学习重点：自学BeautifulSoup，回顾巩固CSS选择器语法   

二、学习目标 
1.  自主学习BeautifulSoup基础用法，掌握页面解析流程；  
2.  复习CSS选择器语法，使用CSS选择器提取网页数据；  
3.  结合课堂requests知识，写出合规防反爬爬虫；  
4.  复用SQLAlchemy代码，将新闻数据存入本地SQLite数据库。
"""
engine = create_engine('sqlite:///gov_news.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.gov.cn/"
}

class News(Base):
    __tablename__ = 'gov_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    link = Column(String(255))
    publish_time = Column(String(255))

Base.metadata.create_all(engine)

def get_news(page):
    url = f"https://www.gov.cn/toutiao/liebiao/?page={page}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 403:
            print(f"第{page}页访问受限，触发反爬")
            return False
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        news_list = soup.select(".news_box .list ul li")
        db = Session()
        for item in news_list:
            title = item.select_one("h4 a").get_text(strip=True)
            href = item.select_one("h4 a")["href"]
            full_link = href  # href已经是完整URL，无需拼接
            pub_time = item.select_one(".date").get_text(strip=True)
            db.add(News(title=title, publish_time=pub_time, link=full_link))
        db.commit()
        db.close()
        print(f"第{page}页抓取完成")
        return True
    except Exception as e:
        print(f"第{page}页异常：{e}")
        return False

def delete_all_news():
    db = Session()
    db.query(News).delete()
    db.commit()
    db.close()
    print("所有新闻数据已删除")

def output_all_news():
    db = Session()
    news = db.query(News).all()
    db.close()
    for item in news:
        print(f"{item.title} - {item.publish_time} - {item.link}")

def output_as_csv():
    db=Session()
    news=db.query(News).all()
    db.close()
    data = [{'id': n.id, 'title': n.title, 'link': n.link, 'publish_time': n.publish_time} for n in news]
    df=pd.DataFrame(data)
    df.to_csv('gov_news.csv',index=False,encoding='utf-8-sig')
    print("新闻数据已导出到gov_news.csv")




if __name__ == "__main__":
    while True:
        print("1.开始抓取新闻数据...")
        print("2.删除所有新闻数据...")
        print("3.输出所有新闻数据...")
        print("4.导出新闻数据到CSV文件...")
        print("5.退出程序...")
        choice = input("请输入您的选择：")
        if choice == "1":
            choice1 = int(input("请输入要抓取的页数："))
            if choice1>=10:print("最多只能抓取10页")
            else:
                for page in range(1, choice1+1):
                    get_news(page)
                    time.sleep(random.uniform(2, 4))
                print("抓取全部完成")
        if choice == "2":
            delete_all_news()
            print("所有新闻数据已删除")
        if choice == "3":
            output_all_news()
        if choice == "4":
            output_as_csv()
        if choice == "5":
            print("程序已退出")
            break
