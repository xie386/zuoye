"""
【程序33】  
题目：打印出杨辉三角形（要求打印出10行如下图）  
1.程序分析：  
1  
1   1  
1   2   1  
1   3   3   1  
1   4   6   4   1  
1   5   10   10   5   1  
"""

row = [1]
for _ in range(10):
    print("   ".join(str(n) for n in row))
    row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
