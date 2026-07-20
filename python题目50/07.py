"""
题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。  
1.程序分析：利用while语句,条件为输入的字符不为 '\n '.  
"""
input_str = input("请输入一行字符：")
letter_count = 0
space_count = 0
digit_count = 0
other_count = 0
for char in input_str:
    if char == '\n':
        break
    if char.isalpha():
        letter_count += 1
    elif char.isspace():
        space_count += 1
    elif char.isdigit():
        digit_count += 1
    else:
        other_count += 1
print(f"英文字母的个数为{letter_count}")
print(f"空格的个数为{space_count}")
print(f"数字的个数为{digit_count}")
print(f"其它字符的个数为{other_count}")
