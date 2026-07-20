"""
【程序14】  
题目：输入某年某月某日，判断这一天是这一年的第几天？  
1.程序分析：以3月5日为例，应该先把前两个月的加起来，
然后再加上5天即本年的第几天，特殊情况，闰年且输入月份大于3时需考虑多加一天。  
"""

input_year = int(input("请输入年份："))
input_month = int(input("请输入月份："))
input_day = int(input("请输入日期："))

def is_leap_year(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0
#每月的天数列表
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
if is_leap_year(input_year):
    month_days[1] = 29

real_day = sum(month_days[:input_month - 1]) + input_day
print(f"{input_year}年{input_month}月{input_day}日是这一年的第{real_day}天")