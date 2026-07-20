"""
【程序27】  
题目：求100之内的素数  
素数定义:大于1的自然数，只能被1和它本身整除的数。
"""
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False
    return True
for i in range(1, 101):
    if is_prime(i):
        print(f"{i}是素数")
