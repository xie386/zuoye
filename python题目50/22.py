"""
【程序22】  
题目：利用递归方法求5!。  
1.程序分析：递归公式：fn=fn_1*4!  
2.程序实现：
"""
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
print(factorial(5))