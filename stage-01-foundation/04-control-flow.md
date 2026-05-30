# 第四章：条件与循环

## 4.1 if 语句：让程序做选择

```python
temperature = 30

if temperature > 35:
    print("太热了！")
elif temperature > 25:
    print("挺舒服的")
else:
    print("有点冷")
```

---

### 4.1.1 缩进就是语法

Python 跟其他语言最大的不同：**缩进决定了代码块的范围。**

```python
# ✅ 正确
if True:
    print("第一行")
    print("第二行")    # 这两行都属于 if
print("第三行")        # 这行不属于 if，无论如何都执行

# ❌ 错误（缩进不一致）
if True:
    print("ok")
  print("bad")    # IndentationError!
```

> 💡 这是 Python 设计者 Guido van Rossum 的信仰：**「代码被读的次数远多于被写的次数」**。强制缩进让所有人的代码都干净整齐。

一般来说用 **4 个空格**，不要用 Tab。VS Code 默认会把 Tab 转成 4 个空格。

---

### 4.1.2 条件判断的底层

```python
if x > 5:
    ...
```

Python 执行这行时的流程：

1. 计算 `x > 5` → 得到一个布尔值（True/False）
2. 如果是 True，进入缩进块
3. 如果是 False，跳到下一个 `elif` 或 `else`
4. 都没有且是 False，跳过整个 if 块

---

## 4.2 while 循环：重复到条件不满足

```python
count = 1
while count <= 5:
    print(f"第{count}次")
    count = count + 1   # 别忘了这个！否则死循环
```

输出：
```
第1次
第2次
第3次
第4次
第5次
```

### ⚠️ 死循环

```python
x = 1
while x > 0:    # 永远为 True
    print("停不下来了...")
```

**按 Ctrl+C 退出。** 每个 while 循环必须有一个「终止条件」和一个「让条件趋近终止的步骤」。

---

## 4.3 for 循环：遍历一个序列

```python
# 遍历字符串
for char in "Hello":
    print(char)
# H
# e
# l
# l
# o

# 遍历数字范围
for i in range(5):
    print(i)
# 0
# 1
# 2
# 3
# 4
```

---

### 4.3.1 range() 详解

```python
range(5)          # 0, 1, 2, 3, 4（不含 5）
range(2, 5)       # 2, 3, 4（从 2 到 4）
range(1, 10, 2)   # 1, 3, 5, 7, 9（步长为 2）
```

> 🧠 range() 在底层**不生成列表**。它是「懒加载」的——每次循环时按需生成下一个数。你 `range(1000000000)` 不会吃满内存。

---

### 4.3.2 enumerate()：同时要索引和值

```python
fruits = ["苹果", "香蕉", "橙子"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: 苹果
# 1: 香蕉
# 2: 橙子
```

这是 Python 里写得最多的循环模式之一。enumerate 的底层：每次迭代返回一个 `(索引, 值)` 的元组。

---

## 4.4 break 和 continue

```python
# break：彻底退出循环
for i in range(10):
    if i == 3:
        break       # 遇到 3，不继续了
    print(i)
# 0
# 1
# 2

# continue：跳过本轮，继续下一轮
for i in range(5):
    if i == 2:
        continue    # 跳过 2
    print(i)
# 0
# 1
# 3
# 4
```

---

## 4.5 实战项目①：猜数字游戏

```python
import random

answer = random.randint(1, 100)
guess = None
attempts = 0

print("我想到一个 1-100 之间的数字，你猜是多少？")

while guess != answer:
    guess = int(input("你的猜测："))
    attempts += 1
    
    if guess > answer:
        print("太大了！")
    elif guess < answer:
        print("太小了！")

print(f"恭喜！答案就是 {answer}，你用了 {attempts} 次。")
```

---

### 这段代码逐行拆解：

| 行 | 作用 |
|----|------|
| `import random` | 加载 random 模块（Python 自带） |
| `random.randint(1,100)` | 生成一个 1-100 的随机整数 |
| `input("你的猜测：")` | 从用户键盘读取输入，返回字符串 |
| `int(...)` | 把字符串变成整数 |
| `attempts += 1` | 等价于 `attempts = attempts + 1` |

> 🔧 小改进：如果用户输入的不是数字呢？我们会在**第八章（异常处理）**里解决。

---

## 4.6 实战项目②：99 乘法表

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j:2}", end="  ")
    print()  # 换行
```

输出：
```
1×1= 1  
1×2= 2  2×2= 4  
1×3= 3  2×3= 6  3×3= 9  
...
```

**关键点**：`end="  "` 让 print 不换行，`print()` 空调用输出一个换行。

---

## 📝 本章练习

1. 写一个 FizzBuzz 程序：遍历 1-100，3 的倍数输出 "Fizz"，5 的倍数输出 "Buzz"，同时是 3 和 5 的倍数输出 "FizzBuzz"，其余输出数字本身。

2. 改进猜数字游戏：限制只能猜 7 次，超次失败。提示用户输入验证。

3. 打印一个金字塔图案（用户输入高度）：
   ```
      *
     ***
    *****
   *******
   ```

---

👉 下一章：[**函数**](05-functions.md) —— 可复用的代码积木
