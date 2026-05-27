# exam_system.py
# 考场管理系统核心逻辑模块

import os
import random
from student import Student


class ExamSys:
    """
    学生信息与考场管理系统类
    """

    def __init__(self, filepath="人工智能编程语言学生名单.txt"):
        """
        系统初始化：加载学生名单，初始化考场安排列表
        """
        self.filepath = filepath      # 学生名单文件路径
        self.students = []            # 存储所有 Student 对象
        self.exam_arrangement = []    # 存储考场安排（打乱后的学生列表）
        self.load_students()          # 自动加载学生信息

    #  功能 1：菜单运行控制
    def run(self):
        """
        系统主循环，显示菜单并根据用户输入调度对应功能函数
        """
        menu = (
            "\n===== 学生信息与考场管理系统 =====\n"
            "1. 查询学生信息\n"
            "2. 随机点名\n"
            "3. 生成考场安排表\n"
            "4. 生成准考证文件\n"
            "+----------------------------------------\n"
            "0. 退出系统"
        )
        # 功能编号 → 对应函数的映射表
        func_map = {
            "1": self.find_student,
            "2": self.random_roll_call,
            "3": self.generate_exam_arrangement,
            "4": self.generate_admission_tickets,
        }
        prompt = "请输入功能编号："
        print(menu)
        while True:
            choice = input(prompt).strip()
            if choice == "0":
                print("感谢使用，系统已退出。再见！")
                break
            elif choice in func_map:
                func_map[choice]()        # 调用对应功能函数
                print(menu)
                prompt = "请输入功能编号："  # 正常执行后重置提示语
            else:
                # 友好错误提示，下一次循环直接以错误提示语作为 input 提示
                prompt = "功能编号不存在，请正确输入功能编号（0~4）："

    #  功能 2：学生信息初始化
    def load_students(self):
        """
        从txt文件中读取学生信息，构造 Student 对象列表
        """
        self.students = []
        if not os.path.exists(self.filepath):
            print(f"[错误] 找不到学生名单文件：{self.filepath}")
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[1:]:  # 跳过首行表头
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            seq, name, gender, cls, student_id, college = (
                parts[0], parts[1], parts[2],
                parts[3], parts[4], parts[5]
            )
            self.students.append(
                Student(seq, name, gender, cls, student_id, college)
            )
        print(f"[系统] 已成功加载 {len(self.students)} 名学生信息。")

    #  功能 3：信息查找和定位
    def find_student(self):
        """
        根据用户输入的学号查询并打印对应学生的完整信息
        """
        student_id = input("请输入要查询的学号：").strip()
        # 遍历列表查找匹配学号
        for stu in self.students:
            if stu.student_id == student_id:
                print("\n查询结果：")
                print(stu)
                return
        # 未找到时的友好提示
        print("未找到该学号对应的学生，请检查输入是否正确。")

    #  功能 4：随机点名
    def random_roll_call(self):
        """
        输入点名人数，随机抽取不重复学生并输出姓名和学号
        使用 try-except 处理以下异常：
          1. 输入非数字字符
          2. 输入人数 <= 0
          3. 输入人数超过学生总人数
        """
        total = len(self.students)
        while True:
            try:
                n = int(input(f"请输入需要点名的学生数量（共 {total} 名学生）：").strip())
                if n <= 0:
                    raise ValueError("点名人数必须大于 0。")
                if n > total:
                    raise ValueError(f"点名人数（{n}）超过学生总人数（{total}），请重新输入。")
            except ValueError as e:
                # 捕获非数字输入（int() 转换失败）以及手动 raise 的 ValueError
                print(f"[输入错误] {e}")
                continue    # 回到循环顶部，让用户重新输入
            break   # 输入合法，跳出循环
        # 随机不重复抽样
        selected = random.sample(self.students, n)
        print("\n本次随机点名结果：")
        for idx, stu in enumerate(selected, start=1):
            print(f"{idx}.{stu.name}  {stu.student_id}")

    #  功能 5：生成考场安排表
    def generate_exam_arrangement(self):
        """
        随机打乱全班学生顺序，生成考场安排表文件（考场安排表.txt）
        """
        if not self.students:
            print("[错误] 学生名单为空，无法生成考场安排表。")
            return
        # 深拷贝列表后打乱顺序，避免修改原始名单
        self.exam_arrangement = self.students[:]
        random.shuffle(self.exam_arrangement)

        output_path = "考场安排表.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            for seat_no, stu in enumerate(self.exam_arrangement, start=1):
                f.write(f"{seat_no},{stu.name},{stu.student_id}\n")

        print(f"[系统] 考场安排表已生成：{os.path.abspath(output_path)}")
        print("考场安排表预览（前5条）：")
        for i, stu in enumerate(self.exam_arrangement[:5], start=1):
            print(f"{i},{stu.name},{stu.student_id}")
        if len(self.exam_arrangement) > 5:
            print(f"... 共 {len(self.exam_arrangement)} 条记录")

    #  功能 6：生成准考证文件
    def generate_admission_tickets(self):
        """
        根据考场安排信息，在 '准考证' 文件夹下为每名学生生成独立准考证文件
        文件命名：01.txt, 02.txt, ...
        文件内容：考场座位号、姓名、学号
        """
        # 检查是否已生成考场安排
        if not self.exam_arrangement:
            print("[提示] 尚未生成考场安排表，正在自动生成...")
            self.generate_exam_arrangement()
            if not self.exam_arrangement:
                return
        # 创建 '准考证' 文件夹（已存在不报错）
        folder_name = "准考证"
        os.makedirs(folder_name, exist_ok=True)   # exist_ok=True 保证不抛出异常

        for seat_no, stu in enumerate(self.exam_arrangement, start=1):
            filename = f"{seat_no:02d}.txt"                     # 01.txt, 02.txt ...
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"考场座位号:{seat_no}\n")
                f.write(f"姓名:{stu.name}\n")
                f.write(f"学号:{stu.student_id}\n")
        print(
            f"[系统] 准考证文件已全部生成！\n"
            f"共生成 {len(self.exam_arrangement)} 份准考证\n"
            f"保存路径：{os.path.abspath(folder_name)}"
        )