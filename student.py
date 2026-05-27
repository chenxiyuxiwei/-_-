# student.py
# 学生类定义模块

class Student:
    """
    学生信息类
    封装单个学生的所有属性信息
    """

    def __init__(self, seq, name, gender, cls, student_id, college):
        """
        初始化学生对象
        :param seq:        序号
        :param name:       姓名
        :param gender:     性别
        :param cls:        班级
        :param student_id: 学号
        :param college:    学院
        """
        self.seq        = seq           # 序号
        self.name       = name          # 姓名
        self.gender     = gender        # 性别
        self.cls        = cls           # 班级
        self.student_id = student_id    # 学号
        self.college    = college       # 学院

    def __str__(self):
        """返回学生信息的格式化字符串"""
        return (
            f"序号: {self.seq}\t"
            f"姓名: {self.name}\t"
            f"性别: {self.gender}\t"
            f"班级: {self.cls}\t"
            f"学号: {self.student_id}\t"
            f"学院: {self.college}"
        )