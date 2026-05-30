# 第三章：数据类型

## 3.1 为什么需要「类型」

计算机底层只有 0 和 1。同样一串 0/1，可以是数字 65，也可以是字母 'A'。**类型**就是告诉计算机：「请用这种视角来解读这一串二进制。」

```python
# 同一个值，不同操作结果不同
x = 100
y = "100"

print(x + 1)     # 101   ← 数字加法
print(y + "1")   # 1001  ← 字符串拼接
print(y + 1)     # TypeError! ← 字符串和数字不能混用
```

---

## 3.2 Python 的四大基础类型

| 类型 | 写法 | 例子 | 通俗理解 |
|------|------|------|---------|
| `int` 整数 | 直接写 | `42`, `-7`, `0` | 数学里的整数 |
| `float` 浮点数 | 带小数点 | `3.14`, `-0.5`, `1.0` | 数学里的小数 |
| `str` 字符串 | 引号包起来 | `"hello"`, `'世界'` | 文字 |
| `bool` 布尔值 | True/False | `True`, `False` | 是/否 |

查看类型：

```python
print(type(42))       # <class 'int'>
print(type(3.14))     # <class 'float'>
print(type("hello"))  # <class 'str'>
print(type(True))     # <class 'bool'>
```

---

## 3.3 整数（int）：没有上限的数字

Python 的 int 有一个其他语言羡慕的特点：

```python
# Python int 可以任意大，只受内存限制
big = 1234567890123456789012345678901234567890
print(big * big)  # 照样能算，不溢出
```

> 💡 C/Java 里 `int` 只能存到 21 亿左右，超过就「溢出」变成负数。Python 没有这个问题——它在底层用了**变长存储**，数字有多大就分配多大内存。

---

## 3.4 浮点数（float）：不精确的小数

这是很多初学者踩的第一个坑：

```python
print(0.1 + 0.2)        # 0.30000000000000004  ← 不是 0.3！
print(0.1 + 0.2 == 0.3) # False
```

**这不是 Python 的 bug，是所有语言都有的问题。** 

原因：计算机用二进制存储小数。0.1 在二进制里是无限循环小数（就像十进制里的 1/3 = 0.333...），存不下，只能截断。截断 → 微小误差 → 你看到的诡异结果。

**怎么正确处理小数？**

```python
# 方法一：比较时用近似
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# 方法二：用 Decimal 处理金钱
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3 ← 精确
```

> 🧠 **实战经验**：涉及金钱计算，永远用 `Decimal` 或把金额转成整数（分）来算。浮点数在金融代码里是定时炸弹。

---

## 3.5 字符串（str）：文字的操作

```python
name = "Alice"

# 拼接
greeting = "Hello, " + name    # "Hello, Alice"

# 重复
line = "-" * 20                # "--------------------"

# 长度
print(len(name))               # 5

# 索引（从 0 开始）
print(name[0])                 # 'A'
print(name[-1])                # 'e' （倒数第一个）

# 切片（取一段）
print(name[0:3])               # 'Ali'（下标 0,1,2，不含 3）
print(name[1:])                # 'lice'（从 1 到末尾）

# 大小写
print(name.upper())            # 'ALICE'
print(name.lower())            # 'alice'
```

---

### 3.5.1 字符串是不可变对象

```python
name = "Alice"
# name[0] = "B"   ← 这会报错！字符串不能修改

# 想改怎么办？创建一个新字符串
name = "B" + name[1:]    # "Blice" （新创建了一个字符串对象）
```

---

### 3.5.2 f-string：字符串格式化的现代写法

```python
name = "小明"
age = 25
print(f"我叫{name}，今年{age}岁")     # 我叫小明，今年25岁
print(f"{name}明年{age + 1}岁")       # 小明明年26岁

# 格式化数字
price = 1234.5678
print(f"价格：{price:.2f}元")         # 价格：1234.57元
```

---

## 3.6 布尔值（bool）：逻辑的基石

```python
is_raining = True
has_umbrella = False

print(5 > 3)          # True
print(5 == 3)         # False
print(5 != 3)         # True（不等于）
print(5 >= 5)         # True

# 逻辑组合
print(True and True)   # True
print(True and False)  # False
print(True or False)   # True
print(not True)        # False
```

---

### 3.6.1 「真值」判断——Python 特有的灵活性

```python
# 非空/非零的东西，在判断时都是 True
print(bool(1))         # True
print(bool("hello"))   # True
print(bool([1, 2]))    # True

# 空的东西是 False
print(bool(0))         # False
print(bool(""))        # False（空字符串）
print(bool([]))        # False（空列表）
print(bool(None))      # False
```

所以你可以写：

```python
name = ""     # 假设用户没填
if name:      # 等价于 if bool(name) == True
    print(f"欢迎，{name}")
else:
    print("请填写名字")
```

---

## 3.7 类型转换

```python
int("42")        # 42（字符串转整数）
float("3.14")    # 3.14（字符串转浮点数）
str(42)          # "42"（整数转字符串）
bool(0)          # False
bool("hello")    # True
```

> ⚠️ `int("abc")` 会报错——Python 不知道怎么把字母变成数字。

---

## 📝 本章练习

1. 写代码计算圆的面积（π × r²）。半径 r 从用户输入获取，结果保留两位小数。
2. 解释 `print(0.1 + 0.2 == 0.3)` 为什么是 False，并给出三种判断相等的正确方法。
3. 用切片操作把字符串 `"Hello, World!"` 变成 `"World! Hello,"`。

---

👉 下一章：[**条件与循环**](04-control-flow.md) —— 让程序会「思考」
