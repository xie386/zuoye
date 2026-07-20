#判断素数的方法：用一个数分别去除2到sqrt(这个数)，如果能被整除，则表明此数不是素数，反之是素数。  
#什么是素数：素数是指大于1的自然数，且只能被1和它本身整除的数。
from math import sqrt


print(sqrt(3))

print("请输入一个数：")
num = int(input())
for i in range(2,int(sqrt(num)+1)):
    if num % i == 0:
        print(f"{num}不是素数")
        break
else:
    print(f"{num}是素数")

