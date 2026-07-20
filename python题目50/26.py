
"""
【程序26】  
题目：请输入星期几的第一个字母来判断一下是星期几，
如果第一个字母一样，则继续   判断第二个字母。  
"""
input_week = input("请输入星期几的第一个字母：")
if input_week == "M":
    print("是星期一")
elif input_week == "T":
    print("是星期二")
elif input_week == "W":
    print("是星期三")
elif input_week == "T":
    print("是星期四")
elif input_week == "F":
    print("是星期五")
elif input_week == "S":
    input_week = input("请输入星期几的第二个字母：")
    if input_week == "A":
        print("是星期六")
    else:
        print("是星期日")
else:
    print("输入错误")
    
