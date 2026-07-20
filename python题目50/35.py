"""
【程序35】  
题目：输入数组，最大的与第一个元素交换，最小的与最后一个元素交换，输出数组。  
1.程序分析：先找到最大的与最小的元素，再交换它们的位置。  
2.程序实现：
"""
list = []
list = list(map(int, input("请输入一个数组：").split()))
print(list)
max_index = list.index(max(list))
min_index = list.index(min(list))
list[max_index], list[0] = list[0], list[max_index]
list[min_index], list[-1] = list[-1], list[min_index]
print(list)