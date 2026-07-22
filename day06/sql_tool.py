import pymysql
class MySqlLUtil:
    def __init__(self,host='localhost',port=3306,user='root',password='123456',db='test'):
        self.conn=pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4'
        )
        self.cursor=self.conn.cursor()
    def query(self,sql,args=None):
        #判断是是应该返回单条结果还是多条结果,true:fetchone,false:fetchall
        self.cursor.execute(sql,args or [])
        sql_upper=sql.upper().strip()
        is_single=any(kw in sql_upper for kw in ['COUNT(','SUM(','AVG(','MAX(','MIN(','LIMIT 1'])
        return self.cursor.fetchone() if is_single else self.cursor.fetchall()
    def execute(self,sql,args=None):
        self.cursor.execute(sql,args or [])
        self.conn.commit()
        return self.cursor.rowcount
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    util=MySqlLUtil(db='ZQK4')
    print(util.query('select * from student'))
    util.close()
