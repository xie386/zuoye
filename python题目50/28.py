"""
【程序28】  
题目：对10个数进行排序  
1.程序分析：可以利用选择法，即从后9个比较过程中，
选择一个最小的与第一个元素交换，   
下次类推，即用第二个元素与后8个进行比较，并进行交换。  
"""
list1 = []
for i in range(1, 11):
    list1.append(int(input(f"请输入第{i}个数：")))

# 选择排序
for i in range(9):
    min_index = i
    for j in range(i + 1, 10):
        if list1[j] < list1[min_index]:
            min_index = j
    # 交换最小值到位置i
    if min_index != i:
        list1[i], list1[min_index] = list1[min_index], list1[i]

print("从小到大排序结果为：", list1)



