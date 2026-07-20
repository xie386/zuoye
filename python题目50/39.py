"""
【程序39】  
题目：编写一个函数，输入n为偶数时，调用函数求1/2+1/4+...+1/n,
当输入n为奇数时，调用函数1/1+1/3+...+1/n

"""

def sum_fraction(n):
    """根据n的奇偶性计算分数和"""
    start = 2 if n % 2 == 0 else 1
    total = 0.0
    for i in range(start, n + 1, 2):
        total += 1 / i
    return total


if __name__ == '__main__':
    print(sum_fraction(6))   # 偶数: 1/2 + 1/4 + 1/6
    print(sum_fraction(7))   # 奇数: 1/1 + 1/3 + 1/5 + 1/7