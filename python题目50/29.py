"""
【程序29】  
题目：不使用numpy库求一个3*3矩阵对角线元素之和  
1.程序分析：利用双重for循环控制输入二维数组，再将a累加后输出。  
"""
#代码实现
a = []
for i in range(3):
    a.append([int(input(f"请输入第{i+1}行第{j+1}列元素：")) for j in range(3)])
print(a)
print("对角线元素之和为：", sum(a[i][i] for i in range(3)))
