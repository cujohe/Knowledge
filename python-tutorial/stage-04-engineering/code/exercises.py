"""
第四阶段配套代码：测试示例、调试示例

运行测试：
    pip install pytest
    pytest test_calculator.py -v
"""

# ============================================================
# calculator.py — 被测试的模块
# ============================================================

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


def calculate_tax(price, rate=0.13):
    """计算含税价格"""
    return round(price * (1 + rate), 2)


# ============================================================
# test_calculator.py — 测试文件
# ============================================================
# 
# 将此文件保存为 test_calculator.py 后运行：
#
#   pip install pytest
#   pytest test_calculator.py -v
#
# 预期结果：全部 PASSED

import pytest
from calculator import add, subtract, multiply, divide, calculate_tax


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)


@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 2),
    (10, 5, 5),
    (0, 5, -5),
    (-3, -2, -1),
])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0


def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)


def test_calculate_tax():
    assert calculate_tax(100) == 113.0
    assert calculate_tax(0) == 0.0


# ============================================================
# debug_demo.py — 调试演示
# ============================================================

def buggy_function(data):
    """故意有 bug 的函数——用来练习调试"""
    result = []
    for item in data:
        # 假设：item 是字典，有 'name' 和 'score' 字段
        # 实际：数据可能没有这些字段
        name = item["name"]
        score = item["score"]
        result.append(f"{name}: {score}")
    return result


def better_function(data):
    """修复后的版本"""
    result = []
    for i, item in enumerate(data):
        try:
            name = item.get("name", f"未知_{i}")
            score = item.get("score", 0)
            result.append(f"{name}: {score}")
        except AttributeError as e:
            print(f"[WARNING] 第 {i} 条数据格式异常：{e}")
    return result


if __name__ == "__main__":
    # 测试 calculator
    print("测试 calculator 模块...")
    assert add(2, 3) == 5, "add 失败"
    assert divide(10, 2) == 5, "divide 失败"
    print("✅ 基本测试通过\n")

    # 演示修复
    bad_data = [
        {"name": "张三", "score": 85},
        {"name": "李四"},  # 缺 score
        "not a dict",      # 根本不是字典
        {"score": 90},     # 缺 name
    ]

    print("原始（有问题的）数据：")
    for d in bad_data:
        print(f"  {d}")

    print("\n修复后的处理结果：")
    for item in better_function(bad_data):
        print(f"  {item}")
