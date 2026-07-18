"""
考试抽象基类模块

定义所有学科考试的共同行为，包括成绩录入、等级评定、加权分计算等。
子类必须实现 get_grade() 抽象方法，可根据各自学科的满分和等级规则进行定制。
"""

import sys
import os

# 添加项目根目录到路径，使直接运行此文件时能找到 shop_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod


class BaseExam(ABC):
    """考试抽象基类，所有学科考试类的父类。
    
    类属性：
        passing_rate: 及格率，默认0.6（即满分的60%为及格线）
    
    实例属性：
        subject_name: 学科名称
        student_name: 学生姓名
        max_score:    满分值
        __score:      私有成绩，默认0
    """

    passing_rate = 0.6

    def __init__(self, subject_name: str, student_name: str, max_score: float):
        """初始化考试实例。
        
        Args:
            subject_name: 学科名称，如"语文"、"数学"、"英语"
            student_name: 学生姓名
            max_score:    满分值
        """
        self.subject_name = subject_name
        self.student_name = student_name
        self.max_score = max_score
        self.__score = 0

    def compare_with_previous(self, previous_score: float):
        """与上一次成绩进行比较，输出进步/退步情况。
        
        Args:
            previous_score: 上一次考试的成绩
        
        Returns:
            tuple: (差值绝对值, 变化百分比(%), 等级是否变化)
        """
        change = abs(self.__score - previous_score)
        change_percent = change / previous_score * 100 if previous_score != 0 else 0
        levelch = (self.get_grade(self.__score) != self.get_grade(previous_score))
        return change, change_percent, levelch

    def get_score(self) -> float:
        """获取当前成绩（私有属性 __score 的 getter）。
        
        Returns:
            float: 当前录入的成绩
        """
        return self.__score

    def input_score(self, score: float):
        """录入成绩，超出满分范围时抛出异常。
        
        Args:
            score: 要录入的成绩
        
        Raises:
            ValueError: 成绩不在 0 到 max_score 之间时抛出
        """
        if score < 0 or score > self.max_score:
            raise ValueError("成绩必须在0到最大成绩之间")
        self.__score = score

    @classmethod
    def set_passing_rate(cls, rate: float):
        """类方法：设置该学科的及格率。
        
        Args:
            rate: 及格率，取值范围 0~1
        
        Raises:
            ValueError: rate 不在 0~1 之间时抛出
        """
        if rate < 0 or rate > 1:
            raise ValueError("及格率必须在0到1之间")
        cls.passing_rate = rate
        print(f"已设置{cls.__name__}的及格率为{rate}")

    @staticmethod
    def check_student_name(name: str) -> bool:
        """静态方法：校验学生姓名是否有效（非空字符串）。
        
        Args:
            name: 待校验的学生姓名
        
        Returns:
            bool: 姓名有效返回 True，否则返回 False
        """
        if not name:
            return False
        return True

    @abstractmethod
    def get_grade(self, score):
        """抽象方法：根据分数评定等级，子类必须实现。
        
        Args:
            score: 成绩分数
        
        Returns:
            str: 等级字符串（"优秀"/"良好"/"及格"/"不及格"）
        """
        pass

    def calc_weight_score(self, weight: float) -> float:
        """计算加权分，如期末成绩占70%时 weight=0.7。
        
        Args:
            weight: 权重系数
        
        Returns:
            float: 加权后的分数
        """
        return self.__score * weight

    def print_score(self):
        """通用成绩单打印，根据及格率判断是否及格。"""
        print(f"{self.student_name}同学的{self.subject_name} 成绩为: {self.__score}", end=" ")
        if self.__score >= self.passing_rate * self.max_score:
            print("及格")
        else:
            print("不及格")
