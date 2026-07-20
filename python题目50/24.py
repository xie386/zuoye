"""
【程序24】  
题目：给一个不多于5位的正整数，要求：一、求它是几位数，二、逆序打印出各位数字。  

"""

input_num = int(input("请输入一个不多于5位的正整数："))
print(f"该数有{len(str(input_num))}位")
print(f"该数的逆序为：{str(input_num)[::-1]}")
