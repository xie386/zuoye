"""
【程序31】  
题目：将一个数组逆序输出。  
1.程序分析：用第一个与最后一个交换。  
2.程序实现：
"""
list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(list)
for i in range(len(list) // 2):
    list[i], list[-i-1] = list[-i-1], list[i]
print(list)