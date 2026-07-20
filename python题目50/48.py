"""
【程序48】  
题目：某个公司采用公用电话传递数据，数据是四位的整数，在传递过程中是加密的，加密规则如下：
每位数字都加上5,然后除以10的余数代替该数字，
再将第一位和第四位交换，第二位和第三位交换。 

输出：加密后的四位整数。
"""

from telnetlib import theNULL
from tempfile import tempdir


input = int(input("请输入四位整数："))
the_1 = input // 1000
the_2 = input // 100 % 10
the_3 = input // 10 % 10
the_4 = input % 10
the_1 = (the_1 + 5) % 10
the_2 = (the_2 + 5) % 10
the_3 = (the_3 + 5) % 10
the_4 = (the_4 + 5) % 10
temp=0
temp=the_1
the_1=the_4
the_4=temp
temp=the_2
the_2=the_3
the_3=temp

the=the_1*1000+the_2*100+the_3*10+the_4
print(the)
