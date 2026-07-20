"""
【程序34】  
题目：输入3个数a,b,c，按大小顺序输出。  
1.程序分析：先判断a是否大于b，再判断b是否大于c，最后判断c是否大于a。  
2.程序实现：
"""
a, b, c = map(int, input("请输入3个整数：").split())
if a > b and a > c:
    print("从小到大排序结果为：", a, b, c)
elif b > a and b > c:
    print("从小到大排序结果为：", b, a, c)
elif c > a and c > b:
    print("从小到大排序结果为：", c, b, a)
else:
    print("输入的数有重复")