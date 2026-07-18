"""
语文学科子类模块

继承 BaseExam，满分150分，独有作文分属性。
等级规则：≥135优秀，≥120良好，≥90及格，<90不及格。
"""

from subjects.base_exam import BaseExam


class ChineseExam(BaseExam):
    """语文学科考试类。
    
    等级规则：
        - ≥135 优秀
        - ≥120 良好
        - ≥90  及格
        - <90  不及格
    
    独有属性：
        essay_score: 作文分，满分60
    """

    def __init__(self, subject_name: str, student_name: str, max_score: float):
        """初始化语文考试实例。
        
        Args:
            subject_name: 学科名称
            student_name: 学生姓名
            max_score:    满分值（通常为150）
        """
        super().__init__(subject_name, student_name, max_score)
        self.essay_score: float = 0.0

    def input_essay_score(self, score: float):
        """录入作文成绩，范围必须在 0~60 之间。
        
        Args:
            score: 作文成绩
        
        Raises:
            ValueError: 作文成绩不在 0~60 之间时抛出
        """
        if score < 0 or score > 60:
            raise ValueError("作文成绩必须在0到60之间")
        self.essay_score = score

    def get_grade(self, score=None) -> str:
        """根据语文等级规则评定等级。
        
        Args:
            score: 成绩分数，为 None 时自动取当前录入成绩
        
        Returns:
            str: 等级（"优秀"/"良好"/"及格"/"不及格"）
        """
        if score is None:
            score = self.get_score()
        if score >= 135 and score <= self.max_score:
            return "优秀"
        elif score >= 120 and score < 135:
            return "良好"
        elif score >= 90 and score < 120:
            return "及格"
        elif score >= 0 and score < 90:
            return "不及格"
        else:
            return "无效成绩，成绩必须在0到最大成绩之间"
