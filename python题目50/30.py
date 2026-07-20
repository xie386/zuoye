"""
【程序30】  
题目：有一个已经排好序的数组。现输入一个数，要求按原来的规律将它插入数组中。  
程序分析：首先判断此数是否大于最后一个数，
然后再考虑插入中间的数的情况，插入后此元素之后的数，依次后移一个位置。  
"""
list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(list)
input_num = int(input("请输入要插入的数："))
if input_num > list[-1]:
    list.append(input_num)
else:
    for i in range(len(list)):
        if input_num < list[i]:
            list.insert(i, input_num)
            break
print(list)