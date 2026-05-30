"""
第一阶段：函数练习 —— 圆面积、质数判断、重写猜数字
"""

import math


def circle_area(radius):
    """计算圆的面积"""
    return math.pi * radius ** 2


def is_prime(n):
    """判断一个数是否为质数"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # 只需检查到 sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def average(*args):
    """计算任意多个数字的平均值"""
    if not args:
        return 0
    return sum(args) / len(args)


# --- 用函数重写的猜数字游戏 ---

def generate_answer(min_val=1, max_val=100):
    """生成随机答案"""
    import random
    return random.randint(min_val, max_val)


def get_guess(attempt_num):
    """从用户读取猜测，返回整数或 None（退出信号）"""
    user_input = input(f"第 {attempt_num} 次猜测：")
    if user_input.lower() == "q":
        return None
    try:
        return int(user_input)
    except ValueError:
        print("请输入有效的数字！")
        return "invalid"


def judge_guess(guess, answer):
    """判断猜测结果，返回提示文字"""
    if guess == answer:
        return "correct"
    elif guess > answer:
        return "high"
    else:
        return "low"


def play_guess_number():
    """主游戏循环"""
    answer = generate_answer()
    attempts = 0

    print("猜数字游戏（1-100），输入 q 退出")

    while True:
        guess = get_guess(attempts + 1)
        if guess is None:
            print(f"答案是 {answer}，下次加油！")
            break
        if guess == "invalid":
            continue

        attempts += 1
        result = judge_guess(guess, answer)

        if result == "correct":
            print(f"🎉 恭喜！答案 {answer}，用了 {attempts} 次！")
            break
        elif result == "high":
            print("📉 太大了！")
        else:
            print("📈 太小了！")


def demo():
    """演示基础函数"""
    print("圆面积（半径 5）：", circle_area(5))
    print("2-20 的质数：", [n for n in range(2, 21) if is_prime(n)])
    print("平均值 (1,2,3,4,5)：", average(1, 2, 3, 4, 5))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "play":
        play_guess_number()
    else:
        demo()
