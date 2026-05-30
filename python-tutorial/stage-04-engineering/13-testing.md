# 第十三章：测试

## 13.1 为什么要写测试

没有测试的开发流程：

```
写代码 → 手动跑一下 → 看起来没错 → 上线 → 用户发现 bug → 修 → 又引入新 bug → ...
```

有测试的开发流程：

```
写代码 → 写测试 → 自动跑 → 看到红灯（测试失败）→ 写代码让它绿 → 提交
任何时候改代码 → 跑全部测试 → 旧的没被破坏 ✅
```

> 💡 **测试不是「额外的工作」，而是「让你能放心改代码的保险」。**

---

## 13.2 你的第一个测试

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

```python
# test_calculator.py
import pytest
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)

def test_divide():
    assert divide(10, 2) == 5
    assert divide(5, 2) == 2.5

def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)
```

运行：
```bash
pip install pytest
pytest test_calculator.py -v
```

输出：
```
test_calculator.py::test_add PASSED
test_calculator.py::test_add_floats PASSED
test_calculator.py::test_divide PASSED
test_calculator.py::test_divide_by_zero PASSED
```

> 🔴🟢 **红灯-绿灯-重构**：先写测试（红灯，还没实现）→ 写代码让测试通过（绿灯）→ 优化代码结构（重构，保持绿灯）。

---

## 13.3 pytest 的核心技巧

### parametrize：一组输入测一个函数

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### fixture：共享测试数据

```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_dir(tmp_path):
    """创建一个临时目录，测试结束自动删除"""
    return tmp_path

@pytest.fixture
def sample_data():
    return [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30},
    ]

def test_write_read_csv(temp_dir, sample_data):
    import csv
    
    filepath = temp_dir / "test.csv"
    
    # 写入
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows(sample_data)
    
    # 读回验证
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 2
    assert rows[0]["name"] == "张三"
```

---

## 13.4 测试该测什么

### ✅ 应该测的

- **核心业务逻辑**：计算、状态变更、数据转换
- **边界条件**：空输入、最大值、最小值
- **错误路径**：文件不存在、网络断开、非法输入
- **刚修好的 bug**：防止重犯（回归测试）

### ❌ 不用测的

- Python 内置函数（`len()` 不会坏）
- 第三方库的实现（你没责任验证 pandas 的 `groupby`）
- 纯数据类（就是几个属性，没有逻辑）

---

## 13.5 衡量测试质量：覆盖率

```bash
pip install pytest-cov
pytest --cov=calculator test_calculator.py
```

它会告诉你哪些代码行被测试跑过、哪些没跑过。目标是核心逻辑**80%+** 覆盖率。

> ⚠️ 100% 覆盖率 ≠ 没有 bug。但低于 60% 确认有很多代码从没被验证过。

---

## 13.6 一个实用的测试文件结构

```
myproject/
├── calculator.py
├── utils.py
└── tests/
    ├── __init__.py
    ├── test_calculator.py
    └── test_utils.py
```

```python
# tests/conftest.py — 共享的 fixture 放这里
import pytest

@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]
```

所有 `test_*.py` 文件自动共享 `conftest.py` 里的 fixture，不用导入。

---

## 📝 本章练习

1. 为第五章的 `calculator` 函数写完整测试，覆盖加减乘除和异常情况。
2. 为你之前写的任意一个函数写 3 个测试用例。
3. 运行 `pytest --cov` 查看覆盖率。

---

👉 下一章：[**调试**](14-debugging.md) —— 当程序出问题时的侦探技巧
