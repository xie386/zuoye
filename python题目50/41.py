"""
【程序41】  
题目：海滩上有一堆桃子，五只猴子来分。
第一只猴子把这堆桃子凭据分为五份，多了一个，这只猴子把多的一个扔入海中，拿走了一份。
第二只猴子把剩下的桃子又平均分成五份，又多了一个，它同样把多的一个扔入海中，拿走了一份，
第三、第四、第五只猴子都是这样做的，问海滩上原来"最少"有多少个桃子？  
"""

# 正向枚举：从1开始逐个尝试，找到满足条件的最小数
peach = 1
while True:
    temp = peach
    valid = True
    for _ in range(5):
        # 扔掉1个后必须能被5整除
        if (temp - 1) % 5 != 0:
            valid = False
            break
        # 拿走1/5，剩下4/5
        temp = (temp - 1) * 4 // 5
    if valid:
        print("海滩上原来最少有", peach, "个桃子")
        break
    peach += 1

# 逆向验证：从最终剩余的桃子开始倒推
temp = peach
for _ in range(5):
    assert (temp - 1) % 5 == 0
    temp = (temp - 1) * 4 // 5
print("验证：第五只猴子离开后剩下", temp, "个桃子")