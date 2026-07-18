"""
subjects 学科包

包含考试系统的各学科类定义：

- BaseExam  : 考试抽象基类，定义通用属性和方法
- ChineseExam : 语文学科子类（满分150分）
- MathExam    : 数学学科子类（满分150分，含附加分）
- EnglishExam : 英语学科子类（满分100分，含听力/阅读/写作分项）

外部可通过 `from subjects import BaseExam, ChineseExam, MathExam, EnglishExam` 统一导入。
"""

from subjects.base_exam import BaseExam
from subjects.english import EnglishExam
from subjects.math import MathExam
from subjects.chinese import ChineseExam
