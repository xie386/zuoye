"""
【程序8】  
题目：求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加有键盘控制。  
1.程序分析：关键是计算出每一项的值。  
"""


def get(i,a):
    ii=10**i
    return a*ii

print("请输入一个数字：",end="")
a = int(input())
n=0
num=0
if 0<a<10:
    for i in range(1,6):
        n+=get(i-1,a)
        print(n)
        num+=n
    print(f"num的值为{num}")
else:
    print("请输入一个非0的10以内的数字")