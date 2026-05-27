# main.py
# 程序入口模块

from exam_system import ExamSys

def main():
    system = ExamSys(filepath="人工智能编程语言学生名单.txt")
    system.run()

if __name__ == "__main__":
    main()