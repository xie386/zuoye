"""
学生成绩管理系统 - 主程序入口

整合所有模块，执行完整的测试流程：

1. 基础得分率计算测试
2. 成绩保存与读取测试
3. 多线程录入测试
4. 设置及格率为 0.65
5. 语文测试（创建、录入成绩、查看作文分、评定等级、保存记录）
6. 数学测试（创建、录入成绩、设置附加分、查看加权分、保存记录）
7. 英语测试（创建、录入成绩、打印分项成绩单、评定等级、保存记录）
8. 优秀学生筛选测试（用字典 + 列表推导式）
9. 成绩单生成器测试
10. 批量统计多态测试（3门学科各1份答卷，遍历调用 calc_weighted_score）

进阶挑战：
- 班级总分排名
- 成绩进步追踪（compare_with_previous）
- 学科均衡度分析（偏科判断）
- 异常处理增强（try...except 包裹所有可能异常的操作）
"""

from subjects import BaseExam, ChineseExam, MathExam, EnglishExam
import grade_utils

if __name__ == "__main__":
    max_chines_math = 150  # 语文/数学满分
    max_english = 100      # 英语满分

    # ===== 创建张三、李四、王五三人各自的考试实例 =====
    try:
        chinese_exam = ChineseExam("语文", "张三", max_chines_math)
        math_exam = MathExam("数学", "张三", max_chines_math)
        english_exam = EnglishExam("英语", "张三", max_english)
        chinese_exam2 = ChineseExam("语文", "李四", max_chines_math)
        math_exam2 = MathExam("数学", "李四", max_chines_math)
        english_exam2 = EnglishExam("英语", "李四", max_english)
        chinese_exam3 = ChineseExam("语文", "王五", max_chines_math)
        math_exam3 = MathExam("数学", "王五", max_chines_math)
        english_exam3 = EnglishExam("英语", "王五", max_english)
    except TypeError as e:
        print(f"[错误] 创建考试实例时参数类型错误: {e}")
    except ValueError as e:
        print(f"[错误] 创建考试实例时参数值错误: {e}")

    # ===== 5. 语文测试 =====
    try:
        chinese_exam.input_score(140)
        chinese_exam.input_essay_score(50)
        print(f"{chinese_exam.student_name}语文等级: {chinese_exam.get_grade()}")
    except ValueError as e:
        print(f"[错误] 张三语文成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 张三语文成绩录入参数类型错误: {e}")

    try:
        chinese_exam2.input_score(130)
        chinese_exam2.input_essay_score(47)
        print(f"{chinese_exam2.student_name}语文等级: {chinese_exam2.get_grade()}")
    except ValueError as e:
        print(f"[错误] 李四语文成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 李四语文成绩录入参数类型错误: {e}")

    try:
        chinese_exam3.input_score(120)
        chinese_exam3.input_essay_score(48)
        print(f"{chinese_exam3.student_name}语文等级: {chinese_exam3.get_grade()}")
    except ValueError as e:
        print(f"[错误] 王五语文成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 王五语文成绩录入参数类型错误: {e}")

    # ===== 6. 数学测试 =====
    try:
        math_exam.input_score(126)
        math_exam.input_bonus_points(8)
        print(f"{math_exam.student_name}数学等级: {math_exam.get_grade()}")
    except ValueError as e:
        print(f"[错误] 张三数学成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 张三数学成绩录入参数类型错误: {e}")

    try:
        math_exam2.input_score(119)
        math_exam2.input_bonus_points(10)
        print(f"{math_exam2.student_name}数学等级: {math_exam2.get_grade()}")
    except ValueError as e:
        print(f"[错误] 李四数学成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 李四数学成绩录入参数类型错误: {e}")

    try:
        math_exam3.input_score(150)
        math_exam3.input_bonus_points(0)
        print(f"{math_exam3.student_name}数学等级: {math_exam3.get_grade()}")
    except ValueError as e:
        print(f"[错误] 王五数学成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 王五数学成绩录入参数类型错误: {e}")

    # ===== 7. 英语测试 =====
    try:
        english_exam.input_score(90)
        english_exam.input_listen_reading_writing_score(20, 50, 20)
        print(f"{english_exam.student_name}英语等级: {english_exam.get_grade()}")
    except ValueError as e:
        print(f"[错误] 张三英语成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 张三英语成绩录入参数类型错误: {e}")

    try:
        english_exam2.input_score(80)
        english_exam2.input_listen_reading_writing_score(15, 50, 15)
        print(f"{english_exam2.student_name}英语等级: {english_exam2.get_grade()}")
    except ValueError as e:
        print(f"[错误] 李四英语成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 李四英语成绩录入参数类型错误: {e}")

    try:
        english_exam3.input_score(65)
        english_exam3.input_listen_reading_writing_score(20, 20, 25)
        print(f"{english_exam3.student_name}英语等级: {english_exam3.get_grade()}")
    except ValueError as e:
        print(f"[错误] 王五英语成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 王五英语成绩录入参数类型错误: {e}")

    # ===== 1. 基础得分率计算测试 =====
    try:
        print("张三各科得分率")
        print(f"语文得分率: {grade_utils.calc_percentage(chinese_exam.get_score(), max_chines_math)}")
        print(f"数学得分率: {grade_utils.calc_percentage(math_exam.get_score(), max_chines_math)}")
        print(f"英语得分率: {grade_utils.calc_percentage(english_exam.get_score(), max_english)}")
    except TypeError as e:
        print(f"[错误] 得分率计算参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 得分率计算失败: {e}")

    # ===== 2. 成绩保存与读取测试 =====
    try:
        grade_utils.input_score_thread_safe(
            chinese_exam.student_name, chinese_exam.subject_name,
            chinese_exam.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            math_exam.student_name, math_exam.subject_name,
            math_exam.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            english_exam.student_name, english_exam.subject_name,
            english_exam.get_score(), max_english)
        grade_utils.input_score_thread_safe(
            chinese_exam2.student_name, chinese_exam2.subject_name,
            chinese_exam2.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            math_exam2.student_name, math_exam2.subject_name,
            math_exam2.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            english_exam2.student_name, english_exam2.subject_name,
            english_exam2.get_score(), max_english)
        grade_utils.input_score_thread_safe(
            chinese_exam3.student_name, chinese_exam3.subject_name,
            chinese_exam3.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            math_exam3.student_name, math_exam3.subject_name,
            math_exam3.get_score(), max_chines_math)
        grade_utils.input_score_thread_safe(
            english_exam3.student_name, english_exam3.subject_name,
            english_exam3.get_score(), max_english)
    except TypeError as e:
        print(f"[错误] 成绩保存参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 成绩保存失败: {e}")

    # ===== 3. 多线程录入测试 =====
    try:
        grade_utils.multi_thread_input_test()
    except Exception as e:
        print(f"[错误] 多线程录入测试失败: {e}")

    try:
        grade_utils.read_all_records()
    except FileNotFoundError:
        print("[提示] 成绩记录文件不存在，尚未保存任何记录")
    except Exception as e:
        print(f"[错误] 读取成绩记录失败: {e}")

    # ===== 4. 设置及格率为 0.65 =====
    for exam, name in [(chinese_exam, "语文"), (math_exam, "数学"), (english_exam, "英语")]:
        try:
            exam.set_passing_rate(0.65)
        except ValueError as e:
            print(f"[错误] 设置{name}及格率失败: {e}")
        except TypeError as e:
            print(f"[错误] 设置{name}及格率参数类型错误: {e}")

    # ===== 8. 优秀学生筛选测试 =====
    try:
        print("优秀学生筛选测试")
        grade_utils.get_excellent_students(grade_utils.student_records, "英语", 90)
    except KeyError as e:
        print(f"[错误] 优秀学生筛选中找不到科目或学生: {e}")
    except TypeError as e:
        print(f"[错误] 优秀学生筛选参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 优秀学生筛选失败: {e}")

    # ===== 10. 批量统计多态测试 =====
    try:
        print("\n批量统计多态测试")
        exam_papers = [
            ChineseExam("语文", "赵六", max_chines_math),
            MathExam("数学", "赵六", max_chines_math),
            EnglishExam("英语", "赵六", max_english),
        ]
        exam_papers[0].input_score(135)
        exam_papers[1].input_score(125)
        exam_papers[1].input_bonus_points(10)
        exam_papers[2].input_score(88)
        weight = 0.7
        for exam in exam_papers:
            weighted = exam.calc_weight_score(weight)
            print(f"{exam.student_name}的{exam.subject_name}加权分(权重{weight}): {weighted}")
    except ValueError as e:
        print(f"[错误] 批量统计测试成绩录入失败: {e}")
    except TypeError as e:
        print(f"[错误] 批量统计测试参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 批量统计测试失败: {e}")

    # ===== 班级排名测试（进阶） =====
    try:
        ranking = grade_utils.calculate_class_ranking(grade_utils.student_records)
        print(f"班级排名: {ranking}")
    except TypeError as e:
        print(f"[错误] 班级排名计算参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 班级排名计算失败: {e}")

    # ===== 成绩进步追踪测试（进阶） =====
    try:
        change, change_percent, levelch = chinese_exam.compare_with_previous(119)
        print(f"{chinese_exam.student_name}的语文等级: {chinese_exam.get_grade()}")
        print(f"与上一次成绩的差值: {change:.2f}，进/退步百分比: {change_percent:.2f}%，"
              f"等级是否变化: {levelch}")
    except ValueError as e:
        print(f"[错误] 成绩比较失败: {e}")
    except TypeError as e:
        print(f"[错误] 成绩比较参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 成绩比较失败: {e}")

    # ===== 偏科判断测试（进阶） =====
    try:
        grade_utils.check_balance(grade_utils.student_records)
    except KeyError as e:
        print(f"[错误] 偏科判断中找不到科目: {e}")
    except TypeError as e:
        print(f"[错误] 偏科判断参数类型错误: {e}")
    except Exception as e:
        print(f"[错误] 偏科判断失败: {e}")
