"""
英语学科子类模块

继承 BaseExam，满分100分，独有听力/阅读/写作分项成绩属性。
等级规则：≥90优秀，≥75良好，≥60及格，<60不及格。
重写 print_report_card() 以打印分项成绩单。
"""

from subjects.base_exam import BaseExam


class EnglishExam(BaseExam):
    """英语学科考试类。
    
    等级规则：
        - ≥90 优秀
        - ≥75 良好
        - ≥60 及格
        - <60 不及格
    
    私有属性：
        __listen_score:  听力成绩
        __reading_score: 阅读成绩
        __writing_score: 写作成绩
    
    重写方法：
        print_report_card(): 打印分项成绩单（听力/阅读/写作）
    """

    def __init__(self, subject_name: str, student_name: str, max_score: float):
        """初始化英语考试实例。
        
        Args:
            subject_name: 学科名称
            student_name: 学生姓名
            max_score:    满分值（通常为100）
        """
        super().__init__(subject_name, student_name, max_score)
        self.__listen_score = 0
        self.__reading_score = 0
        self.__writing_score = 0

    def input_listen_reading_writing_score(self, score1: float, score2: float, score3: float):
        """录入听力、阅读、写作三项分项成绩，三者之和必须等于已录入的总成绩。
        
        Args:
            score1: 听力成绩
            score2: 阅读成绩
            score3: 写作成绩
        
        Raises:
            ValueError: 成绩为负数或三者之和不等于总成绩时抛出
        """
        if score1 < 0 or score2 < 0 or score3 < 0 or score1 + score2 + score3 != self.get_score():
            raise ValueError("听力/阅读/写作成绩总和必须等于总成绩且在0到最大成绩之间")
        self.__listen_score = score1
        self.__reading_score = score2
        self.__writing_score = score3

    def get_listen_score(self) -> float:
        """获取听力成绩。"""
        return self.__listen_score

    def get_reading_score(self) -> float:
        """获取阅读成绩。"""
        return self.__reading_score

    def get_writing_score(self) -> float:
        """获取写作成绩。"""
        return self.__writing_score

    def print_report_card(self):
        """打印英语分项成绩单，包含听力、阅读、写作及总成绩。"""
        print(f"{self.student_name}同学的{self.subject_name} 成绩为: "
              f"听力{self.__listen_score}分, 阅读{self.__reading_score}分, "
              f"写作{self.__writing_score}分, 总成绩{self.get_score()}")

    def get_grade(self, score=None) -> str:
        """根据英语等级规则评定等级。
        
        Args:
            score: 成绩分数，为 None 时自动取当前录入成绩
        
        Returns:
            str: 等级（"优秀"/"良好"/"及格"/"不及格"）
        """
        if score is None:
            score = self.get_score()
        if score >= 90 and score <= self.max_score:
            return "优秀"
        elif score >= 75 and score < 90:
            return "良好"
        elif score >= 60 and score < 75:
            return "及格"
        elif score >= 0 and score < 60:
            return "不及格"
        else:
            return "无效成绩，成绩必须在0到最大成绩之间"
