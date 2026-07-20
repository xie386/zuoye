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
