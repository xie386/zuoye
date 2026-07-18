"""
通用工具函数模块

提供成绩管理系统的公共功能，包括成绩校验、得分率计算、文件持久化、
线程安全录入、班级排名、偏科判断等。
"""

import threading

# ===== 全局共享数据和锁 =====

# 全局共享成绩字典，格式: {"张三": {"语文": 80, "数学": 90, "英语": 85}}
student_records = {}

# 全局互斥锁，用于多线程并发录入成绩时的数据安全
record_lock = threading.Lock()

# ===== 各科目满分值（用于偏科分析中的标准化折算） =====

SUBJECT_MAX_SCORES = {"语文": 150, "数学": 150, "英语": 100}


def check_valid_score(score: float, max_score: float) -> bool:
    """校验成绩是否在合法范围（0 ~ 满分）内。
    
    Args:
        score:     待校验的成绩
        max_score: 满分值
    
    Returns:
        bool: 合法返回 True，否则返回 False
    """
    if 0 <= score <= max_score:
        return True
    else:
        return False


def calc_percentage(score: float, max_score: float) -> float:
    """计算得分率 = 分数 / 满分 × 100%。
    
    Args:
        score:     成绩
        max_score: 满分值
    
    Returns:
        float: 得分率（百分比数值）
    """
    return score / max_score * 100


def save_record(record_info: str):
    """将成绩记录追加写入 exam_records.txt（UTF-8 编码）。
    
    Args:
        record_info: 要写入的成绩记录字符串
    """
    with open('exam_records.txt', 'a', encoding='utf-8') as f:
        f.write(record_info + '\n')


def read_all_records() -> list:
    """读取 exam_records.txt 中的全部成绩记录。
    
    Returns:
        list: 每行记录组成的字符串列表
    """
    with open('exam_records.txt', 'r', encoding='utf-8') as f:
        records = f.readlines()
        return records


def get_excellent_students(score_dict: dict, subject: str, threshold: float):
    """使用列表推导式筛选某科目达到指定阈值的学生。
    
    Args:
        score_dict: 学生成绩字典
        subject:    科目名称
        threshold:  优秀分数线
    """
    good_student = [student for student in score_dict
                    if student_records[student][subject] >= threshold]
    result = f"此次{subject}考试优秀的学生有:{good_student}"
    print(result)
    save_record(result)


def report_card_generator(student_list: list):
    """生成器：惰性生成格式化成绩单字符串。
    
    Args:
        student_list: 学生姓名列表
    
    Yields:
        str: 格式化成绩单字符串，如 "张三的成绩为:{'语文': 80}"
    """
    for student in student_list:
        yield f"{student}的成绩为:{student_records[student]}"


def input_score_thread_safe(student_name: str, subject: str,
                             score: float, max_score: float):
    """线程安全地录入成绩，使用全局锁保护共享字典。
    
    Args:
        student_name: 学生姓名
        subject:      科目名称
        score:        成绩分数
        max_score:    该科目满分值
    """
    if not check_valid_score(score, max_score):
        print(f"成绩{score}不在合法范围内（0~{max_score}）")
        return
    with record_lock:
        if student_name not in student_records:
            student_records[student_name] = {}
        student_records[student_name][subject] = score
        result = f"{student_name}的{subject}成绩为:{score}"
        print(result)
        save_record(result)


def multi_thread_input_test():
    """创建3个线程并发录入成绩，验证线程锁是否正常工作。"""
    t1 = threading.Thread(target=input_score_thread_safe,
                           args=("刘强", "语文", 80, 150))
    t2 = threading.Thread(target=input_score_thread_safe,
                           args=("刘强", "数学", 90, 150))
    t3 = threading.Thread(target=input_score_thread_safe,
                           args=("刘强", "英语", 85, 100))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print(student_records)


def calculate_class_ranking(records_dict: dict) -> list:
    """计算每个学生的总成绩并排序。
    
    Args:
        records_dict: 全班成绩字典，格式 {"张三": {"语文": 80, "数学": 90}}
    
    Returns:
        list: 按总分降序排列的 (学生姓名, 总分) 元组列表
    """
    total_scores = {student: sum(records_dict[student].values())
                    for student in records_dict}
    sorted_students = sorted(total_scores.items(),
                             key=lambda x: x[1], reverse=True)
    return sorted_students


def calculate_standard_deviation(scores: dict) -> float:
    """计算单个学生各科成绩的标准差。
    
    先将各科成绩统一折算为百分制（100 * 得分/满分），
    避免因不同科目满分不同而误判偏科。
    
    Args:
        scores: 单个学生的成绩字典，如 {"语文": 140, "数学": 120, "英语": 90}
    
    Returns:
        float: 标准化后的成绩标准差
    """
    normalized = []
    for subject, score in scores.items():
        max_score = SUBJECT_MAX_SCORES.get(subject, 100)
        normalized.append(100 * score / max_score)
    mean = sum(normalized) / len(normalized)
    variance = sum((x - mean) ** 2 for x in normalized) / len(normalized)
    return variance ** 0.5


def check_balance(student_scores: dict):
    """进行偏科判断，分析学生各科成绩是否均衡。
    
    判断标准：
        - 标准差 < 10：     各科均衡
        - 10 ≤ 标准差 < 20：轻微偏科
        - 标准差 ≥ 20：     严重偏科，并输出具体偏科科目
    
    Args:
        student_scores: 全部学生成绩字典
    """
    for student in student_scores:
        std_dev = calculate_standard_deviation(student_scores[student])
        if std_dev < 10:
            print(f"{student}的各科成绩均衡")
        elif 10 <= std_dev < 20:
            print(f"{student}的各科成绩轻微偏科")
        else:
            print(f"{student}的各科成绩严重偏科，具体偏科科目为：")
            for subject in student_scores[student]:
                if student_scores[student][subject] == min(student_scores[student].values()):
                    print(f"  - {subject}")


# ===== 本模块自测代码 =====
if __name__ == "__main__":
    # 多线程并发录入测试
    multi_thread_input_test()

    # 成绩录入测试（含越界校验）
    input_score_thread_safe("李四", "语文", 10000000, 150)  # 超出满分，应被拦截
    input_score_thread_safe("李四", "英语", 85, 100)
    input_score_thread_safe("李四", "数学", 95, 150)
    input_score_thread_safe("李四", "语文", 80, 150)
    input_score_thread_safe("王五", "数学", 90, 150)
    input_score_thread_safe("王五", "英语", 90, 100)
    input_score_thread_safe("王五", "语文", 90, 150)

    # 优秀学生筛选
    get_excellent_students(student_records, "语文", 90)

    # 班级排名
    ranking = calculate_class_ranking(student_records)
    print(ranking)

    # 成绩单生成器
    for record in report_card_generator(student_records.keys()):
        print(record)
        save_record(record)

    # 偏科判断
    check_balance(student_records)
