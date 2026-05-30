# 第五章：函数

## 5.1 为什么需要函数

没函数之前，代码是这样的：

```python
# 计算圆面积（半径 3）
area1 = 3.14 * 3 ** 2
print(area1)

# 计算圆面积（半径 5）
area2 = 3.14 * 5 ** 2
print(area2)

# 计算圆面积（半径 7）... 烦不烦？
area3 = 3.14 * 7 ** 2
print(area3)
```

有了函数之后：

```python
def circle_area(radius):
    """计算圆的面积"""
    return 3.14 * radius ** 2

print(circle_area(3))
print(circle_area(5))
print(circle_area(7))
```

> 💡 **函数 = 给一段代码起个名字，以后叫名字就能执行。** 这是编程里最朴素的复用手段。

---

## 5.2 函数的解剖

```python
def greet(name):           # ← def 关键字 + 函数名 + (参数名)
    """生成问候语"""       # ← 文档字符串（可选，但强烈建议写）
    return f"Hello, {name}!"  # ← return 返回结果

result = greet("Alice")    # ← 调用函数，拿到返回值
print(result)              # Hello, Alice!
```

---

### 5.2.1 return 到底是什么

```python
def add(a, b):
    result = a + b
    return result       # ← 把 result 的值「扔出去」
    print("这行永远不会执行")  # return 下面的代码被跳过

x = add(3, 4)   # x 接到了 return 扔出来的 7
print(x)        # 7
```

**没写 return 的函数，默认返回 `None`：**

```python
def say_hello():
    print("Hello")

result = say_hello()   # 打印 Hello
print(result)          # None（函数没有 return 东西出来）
```

---

## 5.3 参数的各种写法

### 5.3.1 位置参数

```python
def describe(name, age):
    print(f"{name} is {age} years old")

describe("Bob", 30)     # 位置对应：name="Bob", age=30
```

### 5.3.2 关键字参数（调用时指定名字）

```python
describe(age=30, name="Bob")  # 顺序无所谓，名字对上就行
```

### 5.3.3 默认值

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Alice", "你好"))       # 你好, Alice!
```

> ⚠️ **陷阱**：默认值如果是可变对象（如列表），不要这样写：
> ```python
> # ❌ 错误示范
> def add_item(item, bucket=[]):
>     bucket.append(item)
>     return bucket
> 
> print(add_item(1))  # [1]
> print(add_item(2))  # [1, 2] ← 咦？默认列表被污染了！
> ```
> 
> Python 在**定义函数时**就创建了默认值对象，每次调用共享同一个。正确做法：
> ```python
> def add_item(item, bucket=None):
>     if bucket is None:
>         bucket = []
>     bucket.append(item)
>     return bucket
> ```

---

## 5.4 作用域：变量的「可见范围」

```python
x = 10  # 全局变量

def foo():
    y = 20  # 局部变量，只在 foo 里可见
    print(x)  # 10（能读全局变量）
    print(y)  # 20

foo()
print(x)    # 10
print(y)    # NameError! y 只在 foo 里存在
```

### 修改全局变量的正确姿势

```python
counter = 0

def increment():
    global counter      # 声明我要用全局的 counter
    counter += 1
```

> 💡 **尽量不要用 global。** 如果你需要一个共享的可变状态，用类的属性或传给函数处理后再返回。global 是紧急出口，不是正门。

---

## 5.5 函数是「一等公民」

在 Python 里，函数就是一个对象，跟数字、字符串平起平坐。你可以：

```python
# 把函数赋值给变量
def add(a, b):
    return a + b

operation = add
print(operation(3, 4))   # 7

# 把函数当参数传递
def apply(func, x, y):
    return func(x, y)

print(apply(add, 5, 6))  # 11

# 在函数里定义函数
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

> 🧠 **这个特性是理解后续装饰器、回调、lambda 等高级特性的基础。**

---

## 5.6 一个实战：写一个迷你计算器

```python
def calculator():
    """一个交互式命令行计算器"""
    print("简易计算器（输入 q 退出）")
    while True:
        expr = input("> ")
        if expr.lower() == 'q':
            break
        try:
            result = eval(expr)  # eval 执行字符串里的 Python 代码
            print(f"  = {result}")
        except:
            print("  表达式有误，请重试")

# 不要直接用 eval 处理用户输入！这里只是演示。
# 生产环境请用 ast.literal_eval 或自己解析。
```

### 更安全的版本

```python
def safe_calc():
    print("安全计算器：格式为 '数 运算符 数'（如 3 + 4）")
    print("支持：+ - * / ，输入 q 退出")
    
    while True:
        line = input("> ")
        if line.lower() == 'q':
            break
        
        parts = line.split()
        if len(parts) != 3:
            print("  格式错误，请用：数 运算符 数")
            continue
        
        try:
            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])
            
            if op == '+':
                print(f"  = {a + b}")
            elif op == '-':
                print(f"  = {a - b}")
            elif op == '*':
                print(f"  = {a * b}")
            elif op == '/' and b != 0:
                print(f"  = {a / b}")
            else:
                print("  不支持的运算符或除数为零")
        except ValueError:
            print("  请输入有效数字")
```

---

## 📝 本章练习

1. 写一个函数 `is_prime(n)`，判断 n 是否为质数，返回布尔值。
2. 写一个函数，接收任意个数字（用 `*args`），返回平均值。
3. 用函数重写第四章的猜数字游戏——把每个逻辑块（生成答案、读取猜测、判断结果）拆成独立函数。

---

🎉 **恭喜！你完成了第一阶段！**

现在你可以：
- 理解代码怎么被执行
- 用变量存储和操作数据
- 用条件判断和循环控制程序流向
- 把逻辑封装成可复用的函数

下一步是整个 Python 世界里最实用的部分——**数据处理**。你需要先学**列表、字典、集合**（它们比 int/str 好用 100 倍），然后你会发现自己能做的事情突然多了几十倍。

👉 进入第二阶段：[**列表、字典、集合**](../stage-02-data/06-collections.md)
