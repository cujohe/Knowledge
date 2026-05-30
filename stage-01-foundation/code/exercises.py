"""
第一阶段配套代码：猜数字游戏、九九乘法表、计算器、FizzBuzz
"""

import random


def guess_number():
    """猜数字游戏（1-100）"""
    answer = random.randint(1, 100)
    attempts = 0

    print("我想到一个 1-100 之间的数字，你猜是多少？")
    print("（输入 q 退出）")

    while True:
        user_input = input(f"第 {attempts + 1} 次猜测：")

        if user_input.lower() == "q":
            print(f"答案是 {answer}，下次加油！")
            break

        try:
            guess = int(user_input)
        except ValueError:
            print("请输入有效的数字！")
            continue

        if guess < 1 or guess > 100:
            print("请输入 1-100 之间的数字！")
            continue

        attempts += 1

        if guess == answer:
            print(f"🎉 恭喜！答案就是 {answer}，你用了 {attempts} 次。")
            break
        elif guess > answer:
            print("📉 太大了！")
        else:
            print("📈 太小了！")


def multiplication_table():
    """打印 9×9 乘法表"""
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{j}×{i}={i*j:2}", end="  ")
        print()


def fizzbuzz():
    """FizzBuzz：3 的倍数输出 Fizz，5 的倍数输出 Buzz"""
    for num in range(1, 101):
        if num % 15 == 0:
            print("FizzBuzz", end=" ")
        elif num % 3 == 0:
            print("Fizz", end=" ")
        elif num % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(num, end=" ")
        
        if num % 10 == 0:
            print()  # 每 10 个换行


def safe_calculator():
    """安全的命令行计算器"""
    print("安全计算器（格式：数 运算符 数，如 3 + 4）")
    print("支持 + - * /，输入 q 退出\n")

    while True:
        line = input("> ")
        if line.lower() == "q":
            break

        parts = line.split()
        if len(parts) != 3:
            print("  格式错误，请用：数 运算符 数")
            continue

        try:
            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])

            if op == "+":
                print(f"  = {a + b}")
            elif op == "-":
                print(f"  = {a - b}")
            elif op == "*":
                print(f"  = {a * b}")
            elif op == "/":
                if b == 0:
                    print("  除数不能为零")
                else:
                    print(f"  = {a / b}")
            else:
                print(f"  不支持的运算符：{op}")
        except ValueError:
            print("  请输入有效的数字")


def pyramid(height):
    """打印金字塔"""
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)


if __name__ == "__main__":
    print("=== 第一阶段练习代码 ===\n")
    print("1. 猜数字游戏")
    print("2. 9×9 乘法表")
    print("3. FizzBuzz")
    print("4. 计算器")
    print("5. 金字塔\n")

    choice = input("选择要运行的练习 (1-5): ")
    print()

    if choice == "1":
        guess_number()
    elif choice == "2":
        multiplication_table()
    elif choice == "3":
        fizzbuzz()
    elif choice == "4":
        safe_calculator()
    elif choice == "5":
        try:
            h = int(input("金字塔高度："))
            pyramid(h)
        except ValueError:
            print("请输入有效数字")
