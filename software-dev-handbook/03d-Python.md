# 第三部分·四：Python

> Python is an experiment in how much freedom programmers need.  
> Too much freedom and nobody can read another's code;  
> too little and expressiveness is endangered.  
> —— Guido van Rossum

---

## 3d.1 Python 的执行模型

Python 的执行方式和之前讲的 C/Java 都不一样。它是**动态语言**的一类代表。

```
Python 源代码（.py）
    ↓ Python 解释器
字节码（.pyc）  ← Python 内部格式，不是 CPU 指令
    ↓ PVM（Python 虚拟机）
执行
```

和 Java 的对比：

| | Java | Python |
|:---|:---|:---|
| **编译时机** | 显式（javac） | 隐式（import 时自动生成 .pyc） |
| **类型检查** | 编译期（静态类型） | 运行时（动态类型） |
| **虚拟机** | JVM（高度优化的工业级 VM） | PVM（相对简单） |
| **并发模型** | 真正的多线程 | GIL（全局解释器锁）限制 |

### 动态类型的含义

```python
# Python：变量没有类型，值是啥类型它就是啥类型
x = 42          # x 现在是 int
x = "hello"     # x 现在是 str —— 完全合法！
x = [1, 2, 3]   # x 现在是 list

# Java：变量有固定的类型声明
int x = 42;
x = "hello";    // 编译错误！类型不匹配
```

这种灵活性让 Python 开发极快，但也意味着很多错误只能在**运行时**被发现——程序跑到了那一行才知道类型对不上。这也解释了为什么 Python 的单元测试如此重要：测试覆盖了类型检查器本该做的工作。

### GIL（全局解释器锁）

Python 有一个臭名昭著的限制：**同一时刻，只有一个线程能执行 Python 字节码。**

```python
# 即使你创建了多个线程，CPU 密集型任务也不会并行加速
import threading

def count():
    for i in range(10_000_000):
        pass

# 两个线程交替执行，不会真正并行
t1 = threading.Thread(target=count)
t2 = threading.Thread(target=count)
t1.start(); t2.start()
t1.join(); t2.join()
# 总时间 ≈ 单线程时间 × 2（甚至更慢，因为切换有开销）
```

这不是 bug，是设计取舍。GIL 让 CPython 的内存管理（引用计数）变得简单安全，避免了 C/C++ 那种复杂的数据竞争问题。代价是 CPU 密集型多线程无法利用多核。

**绕过 GIL 的方法**：对于 CPU 密集型任务，用 `multiprocessing`（多进程，每个进程有独立的 GIL）；对于 I/O 密集型（网络请求、文件读写），GIL 在 I/O 操作时释放，多线程仍然有效。

---

## 3d.2 一切皆对象

Python 中，**万物皆对象**——包括整数、函数、类本身：

```python
# 数字是对象
x = 42
print(type(x))           # <class 'int'>
print(x.__add__(3))      # 45 —— 你没看错，+ 号本质是调用 __add__ 方法

# 函数是对象
def greet(name):
    return f"Hello, {name}"

print(type(greet))       # <class 'function'>
say_hi = greet           # 函数可以赋值给变量
print(say_hi("World"))   # Hello, World

# 类本身也是对象
print(type(list))        # <class 'type'>
```

这个设计的一致性非常优美：无论你操作什么，它们都遵循相同的对象模型。

---

## 3d.3 核心数据结构

Python 内置了四种功能极强的数据结构：

```python
# list：动态数组，最常用
fruits = ["apple", "banana", "cherry"]
fruits.append("date")           # 尾部增加
fruits.insert(1, "blueberry")   # 指定位置插入
first = fruits.pop(0)           # 弹出并返回第一个元素

# tuple：不可变序列
point = (3, 4)         # 创建后不能修改
x, y = point           # 解包（unpacking）

# dict：哈希表，键值对
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}
config["timeout"] = 30  # 新增键值对
host = config.get("host", "default")  # 安全获取，不存在返回默认值

# set：无序不重复集合
tags = {"python", "tutorial", "beginner"}
tags.add("programming")        # 添加
tags.add("python")             # 重复的，不会加入
intersection = tags & {"tutorial", "advanced"}  # 集合运算
```

---

## 3d.4 函数式特性

Python 融合了面向对象和函数式风格，让代码既灵活又简洁：

```python
# 列表推导式（list comprehension）—— Python 的标志性语法
squares = [x**2 for x in range(10)]           # 0, 1, 4, 9, ..., 81
evens = [x for x in range(20) if x % 2 == 0]  # 带条件过滤

# 字典推导式
word_lengths = {word: len(word) for word in ["hi", "hello", "world"]}

# 生成器（generator）—— 惰性计算，不一次性加载全部数据
def fibonacci():
    a, b = 0, 1
    while True:
        yield a       # 不是 return！函数暂停在这里
        a, b = b, a + b

fib = fibonacci()
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1
print(next(fib))  # 2
# 理论上可以无限生成，但每次只计算下一个值——内存占用极小！
```

生成器是 Python 处理大数据流的秘密武器。读一个 10GB 的文件？用生成器一行一行读，内存里永远只存当前行。

### Lambda（匿名函数）

```python
# 排序时临时定义一个比较规则
users = [{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}]
users.sort(key=lambda u: u["age"])  # 按年龄排序
```

Python 的 lambda 只能写一个表达式，不能包含多行语句。这是刻意限制——如果需要复杂逻辑，就正经定义一个函数，保持代码可读。

---

## 3d.5 面向对象（Python 风格）

```python
class BankAccount:
    # 类变量（所有实例共享）
    bank_name = "MyBank"

    def __init__(self, owner, balance=0):    # 构造函数
        self.owner = owner                   # 实例变量
        self._balance = balance              # _ 开头约定为「受保护」的

    @property
    def balance(self):                       # getter
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self._balance += amount

    def __str__(self):                       # 类似 Java 的 toString()
        return f"{self.owner}: ¥{self._balance}"


class SavingsAccount(BankAccount):           # 继承
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)     # 调用父类构造函数
        self.interest_rate = interest_rate

    def add_interest(self):
        self._balance *= (1 + self.interest_rate)
```

Python 没有 `private` 关键字。`_name` 是约定（靠自觉），`__name` 会触发名称重整（name mangling）以防止子类意外覆盖——但仍然是可访问的。Python 的设计哲学是「我们都是成年人了」（We are all consenting adults）——信任程序员而不是用编译器强制限制。

---

## 3d.6 虚拟环境与包管理

Python 的包管理经历过一段混乱时期，现在趋于统一：

### 问题：依赖冲突

项目 A 需要 `requests==2.25`，项目 B 需要 `requests==2.31`。如果都装在全系统，就会打架。

### 解决方案：虚拟环境

```bash
# 创建虚拟环境
python3 -m venv myproject_env

# 激活虚拟环境
source myproject_env/bin/activate   # Linux/macOS
# myproject_env\Scripts\activate    # Windows

# 在虚拟环境里安装的包，与系统和其他项目完全隔离
pip install requests pandas numpy

# 记录依赖
pip freeze > requirements.txt    # 导出所有依赖和版本

# 另一台机器上复现环境
pip install -r requirements.txt  # 一键安装所有依赖
```

### 现代工具

| 工具 | 作用 |
|:---|:---|
| **pip** | 从 PyPI（Python 包索引）安装包 |
| **venv** | 创建轻量虚拟环境（Python 内置） |
| **poetry** | 现代依赖管理 + 打包（类似 Rust 的 Cargo） |
| **conda** | 科学计算生态的包管理（不仅限于 Python） |
| **uv** | Rust 写的超快 pip 替代品（2024 年新星） |

---

## 3d.7 为什么 Python 这么慢，却这么流行？

```python
# 一段 C 写的高性能代码，用 Python 调用
import numpy as np

# 表面上是 Python，底层是 C/Fortran 的向量化运算
data = np.random.randn(10_000_000)
result = np.mean(data)  # 近 C 的速度
```

Python 的流行遵循一个核心模式：**用 Python 做「胶水」，粘合底层高性能库。**

| 领域 | Python 调用 | 底层实现 |
|:---|:---|:---|
| 数值计算 | NumPy | C + Fortran + BLAS/LAPACK |
| 机器学习 | TensorFlow/PyTorch | C++ + CUDA |
| Web 服务 | Flask/FastAPI + Gunicorn | C 写的 WSGI 服务器 |
| 数据分析 | pandas | NumPy（C）+ 部分 Cython |

Python 的角色不是「快」，而是「让你写起来快」。核心计算由 C/C++ 完成，Python 只负责编排流程。你写一小时 Python 能搞定的事，可能要用 C 写一整天——而这个时间差决定了项目的成败。

---

## 3d.8 从入门到熟练：Python 学习路径

### 阶段一：基础语法（1-2 周）

Python 以「学习曲线平缓」著称：
- 变量、基本类型、控制流
- 函数定义和调用
- list、dict、set、tuple 的用法
- 文件读写
- **关键练习**：写一个命令行待办事项管理器

### 阶段二：Pythonic 思维（2-4 周）

- 列表/字典/集合推导式
- 生成器和 yield
- 装饰器（@decorator）
- with 语句和上下文管理器
- 异常处理的最佳实践
- **关键练习**：重构阶段一的代码，让它更 Pythonic

### 阶段三：工程化（4-8 周）

- 虚拟环境与依赖管理
- 模块和包的组织
- 单元测试（pytest）
- 面向对象编程
- 常用标准库（os、sys、json、datetime、pathlib、logging）
- **关键练习**：用 Flask 或 FastAPI 写一个 REST API

### 阶段四：专业方向（按需选择）

| 方向 | 核心库 |
|:---|:---|
| **Web 后端** | FastAPI / Django + SQLAlchemy / PostgreSQL |
| **数据科学** | NumPy + pandas + matplotlib + Jupyter |
| **机器学习** | scikit-learn + PyTorch / TensorFlow |
| **自动化/DevOps** | subprocess + fabric + ansible |
| **爬虫** | requests + BeautifulSoup / Scrapy |

---

## 3d.9 Python 的应用领域

| 领域 | 为什么是 Python |
|:---|:---|
| **AI/机器学习** | PyTorch、TensorFlow 的 Python API + 科研社区的惯性 |
| **数据科学** | pandas、NumPy、Jupyter Notebook 的交互式探索能力 |
| **Web 后端** | Django/Flask/FastAPI 的快速开发 |
| **自动化脚本** | 写一次跑几百次的脚本，开发效率远比运行效率重要 |
| **教育** | 语法简单，适合编程入门（这也是它最初的定位） |
| **科学计算** | 替代 MATLAB，开源免费 |