"""
第二阶段配套代码：词频统计、日记本、CSV 处理、待办事项
"""

import re
import json
import csv
import datetime
from pathlib import Path


def word_counter(text):
    """统计词频，返回排序后的列表"""
    words = re.findall(r"\b\w+\b", text.lower())
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return sorted(word_count.items(), key=lambda x: x[1], reverse=True)


def demo_word_counter():
    text = """
    Python is great. Python is easy to learn. 
    Learn Python today. Python, Python, Python!
    """
    results = word_counter(text)
    for word, count in results:
        print(f"  {word}: {count}")


class Diary:
    """日记本类"""

    def __init__(self, filename="diary.txt"):
        self.filename = filename

    def write(self):
        content = input("今天想写点什么？\n> ")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"\n--- {timestamp} ---\n")
            f.write(f"{content}\n")
        print("✅ 已保存！")

    def read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read()
                if content:
                    print(content)
                else:
                    print("还没有写过日记呢。")
        except FileNotFoundError:
            print("还没有写过日记呢。")

    def run(self):
        while True:
            cmd = input("\n日记本 [w=写, r=读, q=退出]: ").lower()
            if cmd == "w":
                self.write()
            elif cmd == "r":
                self.read()
            elif cmd == "q":
                break
            else:
                print("请输入 w / r / q")


def create_sample_csv(filename="sample_users.csv"):
    """创建示例 CSV 文件"""
    data = [
        ["姓名", "年龄", "城市", "工资"],
        ["张三", 25, "北京", 15000],
        ["李四", 30, "上海", 20000],
        ["王五", 28, "广州", 18000],
        ["赵六", 35, "深圳", 25000],
        ["孙七", 22, "成都", 12000],
    ]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"✅ 已创建：{filename}")


def read_csv(filename="sample_users.csv"):
    """读取 CSV 并用 DictReader 遍历"""
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"  {row['姓名']}, {row['年龄']}岁, {row['城市']}, 月薪 {row['工资']}")


class TodoList:
    """待办事项管理"""

    def __init__(self, filename="todo.json"):
        self.filename = filename
        self.tasks = self._load()

    def _load(self):
        try:
            return json.loads(Path(self.filename).read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        Path(self.filename).write_text(json.dumps(self.tasks, ensure_ascii=False, indent=2))

    def add(self, task):
        self.tasks.append({"task": task, "done": False})
        self._save()
        print(f"✅ 已添加：{task}")

    def list_tasks(self):
        if not self.tasks:
            print("任务列表是空的")
            return
        for i, t in enumerate(self.tasks, 1):
            status = "✅" if t["done"] else "⬜"
            print(f"  {i}. {status} {t['task']}")

    def done(self, index):
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1]["done"] = True
            self._save()
            print(f"✅ 标记完成：{self.tasks[index - 1]['task']}")

    def remove(self, index):
        if 1 <= index <= len(self.tasks):
            removed = self.tasks.pop(index - 1)
            self._save()
            print(f"🗑️  已删除：{removed['task']}")

    def run(self):
        while True:
            cmd = input("\n待办事项 [a=添加, l=列出, d=完成, r=删除, q=退出]: ").lower()
            if cmd == "a":
                self.add(input("任务内容："))
            elif cmd == "l":
                self.list_tasks()
            elif cmd == "d":
                try:
                    self.done(int(input("完成任务编号：")))
                except (ValueError, IndexError):
                    print("请输入有效编号")
            elif cmd == "r":
                try:
                    self.remove(int(input("删除任务编号：")))
                except (ValueError, IndexError):
                    print("请输入有效编号")
            elif cmd == "q":
                break


if __name__ == "__main__":
    print("=== 第二阶段练习代码 ===\n")
    print("1. 词频统计演示")
    print("2. 日记本")
    print("3. 创建示例 CSV + 读取")
    print("4. 待办事项\n")

    choice = input("选择 (1-4): ")
    print()

    if choice == "1":
        demo_word_counter()
    elif choice == "2":
        Diary().run()
    elif choice == "3":
        create_sample_csv()
        print("\n读取内容：")
        read_csv()
    elif choice == "4":
        TodoList().run()
