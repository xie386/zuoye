"""
题目：一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在   
第10次落地时，共经过多少米？第10次反弹多高？
"""
height = 100
distance = 0
for i in range(1,11):
    distance += height
    height /= 2
print(f"第10次落地时，共经过{distance}米")
print(f"第10次反弹高度为{height}米")