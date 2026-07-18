"""
数学学科子类模块

继承 BaseExam，满分150分，独有私有附加分属性。
等级规则：≥140优秀，≥120良好，≥90及格，<90不及格。
加权分计算包含附加分。
"""

from subjects.base_exam import BaseExam


class MathExam(BaseExam):
    """数学学科考试类。
    
    等级规则：
        - ≥140 优秀
        - ≥120 良好
        - ≥90  及格
        - <90  不及格
    
    私有属性：
        __bonus_points: 附加分，默认0，范围0~15
    
    重写方法：
        calc_weight_score: 加权分计算包含附加分
    """

    def __init__(self, subject_name: str, student_name: str, max_score: float):
        """初始化数学考试实例。
        
        Args:
            subject_name: 学科名称
            student_name: 学生姓名
            max_score:    满分值（通常为150）
        """
        super().__init__(subject_name, student_name, max_score)
        self.__bonus_points = 0

    def get_bonus_points(self) -> float:
        """获取附加分（私有属性 __bonus_points 的 getter）。
        
        Returns:
            float: 当前附加分
        """
        return self.__bonus_points

    def input_bonus_points(self, points: float):
        """录入附加分，范围必须在 0~15 之间。
        
        Args:
            points: 附加分
        
        Raises:
            ValueError: 附加分不在 0~15 之间时抛出
        """
        if points < 0 or points > 15:
            raise ValueError("附加分分必须在0到15之间")
        self.__bonus_points = points

    def get_grade(self, score=None) -> str:
        """根据数学等级规则评定等级。
        
        Args:
            score: 成绩分数，为 None 时自动取当前录入成绩
        
        Returns:
            str: 等级（"优秀"/"良好"/"及格"/"不及格"）
        """
        if score is None:
            score = self.get_score()
        if score >= 140 and score <= self.max_score:
            return "优秀"
        elif score >= 120 and score < 140:
            return "良好"
        elif score >= 90 and score < 120:
            return "及格"
        elif score >= 0 and score < 90:
            return "不及格"
        else:
            return "无效成绩，成绩必须在0到最大成绩之间"

    def calc_weight_score(self, weight: float) -> float:
        """计算数学加权分，基数含附加分。
        
        Args:
            weight: 权重系数
        
        Returns:
            float: (成绩 + 附加分) * 权重
        """
        return (self.get_score() + self.__bonus_points) * weight
