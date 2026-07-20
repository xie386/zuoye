"""
【程序45】  
题目：判断一个素数能被几个9整除  

题目错误原因:答案恒为0,故程序无实际意义
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
"""