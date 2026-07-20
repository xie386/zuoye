"""
【程序25】  
题目：一个5位数，判断它是不是回文数。
即12321是回文数，个位与万位相同，十位与千位相同。  
"""
input_num = int(input("请输入一个5位数："))
if str(input_num) == str(input_num)[::-1]:
    print("该数是回文数")
else:
    print("该数不是回文数")