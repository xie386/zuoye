"""
import pymysql
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    charset="utf8mb3",
    port=3306
)
cursor=conn.cursor()
sql1="Create database if not exists ZQK4"
sql2="use ZQK4"
sql3="Create table if not exists student(id int primary key auto_increment,name varchar(20),age int)"
cursor.execute(sql1)
cursor.execute(sql2)
cursor.execute(sql3)
conn.close()
"""

import pymysql
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    charset="utf8mb3",
    database="ZQK4",
    port=3306
)

cursor=conn.cursor()
sql_list=[]
#进行创建表,对表增删改查操作
sql_list.append("use ZQK4")
sql_list.append("Create table if not exists student(id int primary key auto_increment,name varchar(20),age int)")
#(增)插入10个学生
sql_list.append("insert into student(name,age) values('张三',18)")
sql_list.append("insert into student(name,age) values('李四',19)")
sql_list.append("insert into student(name,age) values('王五',20)")
sql_list.append("insert into student(name,age) values('赵六',21)")
sql_list.append("insert into student(name,age) values('王二',22)")
sql_list.append("insert into student(name,age) values('赵三',23)")
sql_list.append("insert into student(name,age) values('王四',24)")
sql_list.append("insert into student(name,age) values('赵五',25)")
sql_list.append("insert into student(name,age) values('王二',26)")
sql_list.append("insert into student(name,age) values('赵三',27)")
#(查)查询所有学生
sql_list.append("select * from student")
#(改)修改张三的年龄为20
sql_list.append("update student set age=20 where id=1")
sql_list.append("select * from student")
#(删)删除张三
sql_list.append("delete from student where id=1")
sql_list.append("select * from student")
#(查)查询所有22岁以上的学生
sql_list.append("select * from student where age>=22")
#(查)查询所有22岁以下的学生
sql_list.append("select * from student where age<22")
sql_list.append("select * from student where age between 18 and 22")
for sql in sql_list:
    print("="*30)
    cursor.execute(sql)
    print(sql)
    if sql.startswith("select"):
        print("查询结果:")
        print(cursor.fetchall())

print("="*30)
conn.close()
