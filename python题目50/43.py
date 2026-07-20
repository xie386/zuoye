"""
【程序43】  
题目：求八位以内0—7所能组成的奇数个数。  
"""
count=0
for a in range(1,99999999):
    # 提取各个位的数字
    digits = [int(digit) for digit in str(a)]
    # 检查是否有(0-7)外的数字
    if any(digit not in range(0,8) for digit in digits):
        continue
    # 检查个位是否为1,3,5,7
    if a % 10 == 1 or a % 10 == 3 or a % 10 == 5 or a % 10 == 7:
        count += 1
        print(a)
print(count,"个(0-7)组成的八位以内奇数")        
