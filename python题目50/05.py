"""
【程序5】  
题目：利用条件运算符的嵌套来完成此题：学习成绩> =90分的同学用A表示，
60-89分之间的用B表示，60分以下的用C表示。  

1.程序分析：(a> b)?a:b这是条件运算符的基本例子。  

"""

print("请输入一个成绩：")
score = int(input())
grade = "A" if score>90 else "B" if score>=60 and score<=89 else "C"
print(f"成绩为{score}的等级为{grade}")
