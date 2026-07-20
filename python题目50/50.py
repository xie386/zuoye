"""
【程序50】  
题目：有五个学生，每个学生有3门课的成绩，从键盘输入以上数据（包括学生号，姓名，三门课成绩），
计算出平均成绩，把有的数据和计算出的平均分数存放在磁盘文件 "stud "中。
"""


for i in range(5):
    scores = []
    NO = input(f"输入第{i+1}个学生的学生号：")
    name = input(f"输入第{i+1}个学生的姓名：")
    for j in range(3):
        scores.append(int(input(f"输入第{i+1}个学生的第{j+1}门课成绩：")))
    avg = sum(scores) / len(scores)
    with open("std.txt", "a", encoding="utf-8") as f:
        f.write(f"学号{NO},姓名{name},成绩{scores},平均分{avg}\n")
