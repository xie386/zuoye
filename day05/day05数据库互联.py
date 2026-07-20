import pymysql

conn = pymysql.connect(
    host="192.168.0.31",
    port=3306,
    user="root",
    password="123456",
    database="zhouqikun",
    charset="utf8mb4"
)
cursor = conn.cursor()
# 示例查询
cursor.execute("SELECT * FROM student;")
print(cursor.fetchall())
# 释放资源
cursor.close()
conn.close()