# 第九章：模块与包

## 9.1 什么是模块

任何一个 `.py` 文件就是一个模块。模块就是**把相关的函数和变量封装在一起**。

```
project/
├── main.py          ← 主程序
├── utils.py         ← 工具函数模块
└── models.py        ← 数据模型模块
```

---

### 9.1.1 创建和使用模块

**utils.py:**
```python
# utils.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

PI = 3.14159
```

**main.py:**
```python
# main.py
import utils                      # 导入整个模块

print(utils.add(3, 4))            # 7
print(utils.multiply(5, 6))       # 30
print(utils.PI)                   # 3.14159
```

---

### 9.1.2 三种导入方式

```python
# 方式一：导入整个模块（推荐，不会污染命名空间）
import utils
utils.add(3, 4)

# 方式二：导入特定名字
from utils import add, PI
add(3, 4)      # 直接用，不用写 utils.

# 方式三：导入全部（不推荐，容易命名冲突）
from utils import *
add(3, 4)      # 你不知道 add 是从哪来的
```

### 9.1.3 别名

```python
import numpy as np          # 数学计算库的通用别名
import pandas as pd         # 数据分析库的通用别名
import matplotlib.pyplot as plt  # 画图库的子模块别名
```

---

## 9.2 模块搜索路径

当你 `import utils` 时，Python 按顺序在这些地方找：

1. **当前目录**（你运行脚本的地方）
2. **PYTHONPATH 环境变量**里的目录
3. **标准库目录**（Python 自带的模块，如 `os`, `json`, `csv`）
4. **第三方包安装目录**（`pip install` 装的东西）

```python
import sys
print(sys.path)   # 看看 Python 在哪些地方找模块
```

---

## 9.3 Python 标准库速览

Python 自带了非常丰富的「电池」。以下是你应该先知道的：

| 模块 | 用途 | 什么时候用 |
|------|------|-----------|
| `os` | 操作系统接口，文件路径操作 | 拼接路径、遍历目录 |
| `sys` | 系统参数，命令行参数 | 读 `sys.argv` |
| `json` | JSON 序列化/反序列化 | 读配置、存数据 |
| `csv` | CSV 文件读写 | 处理 Excel 导出的数据 |
| `datetime` | 日期时间处理 | 时间戳、格式化日期 |
| `re` | 正则表达式 | 文本匹配、提取 |
| `random` | 随机数 | 抽奖、测试数据生成 |
| `math` | 数学函数 | 三角函数、对数、向上取整 |
| `pathlib` | 现代化的路径操作 | 替代 os.path，更好用 |
| `argparse` | 命令行参数解析 | 写命令行工具 |

---

### 9.3.1 pathlib：你应该停止用字符串拼路径

```python
# ❌ 老旧写法（容易在不同操作系统出错）
path = "data" + os.sep + "2024" + os.sep + "report.csv"

# ✅ 现代写法
from pathlib import Path

path = Path("data") / "2024" / "report.csv"
print(path)                          # data/2024/report.csv

# 常用操作
path.exists()                        # 文件存在吗？
path.parent                          # 上级目录：data/2024
path.name                            # 文件名：report.csv
path.suffix                          # 后缀：.csv
path.stem                            # 文件名（不带后缀）：report
path.read_text(encoding="utf-8")     # 读文本
path.write_text("content", encoding="utf-8")  # 写文本
```

---

## 9.4 什么是包

包就是**包含 `__init__.py` 的目录**。它让你把多个模块组织成层级结构。

```
mypackage/
├── __init__.py          ← 标识这是一个包（Python 3.3+ 可省略）
├── core.py
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   └── file_utils.py
└── models/
    ├── __init__.py
    └── user.py
```

导入使用：

```python
from mypackage.core import some_function
from mypackage.utils.math_utils import add
```

---

## 9.5 第三方包管理：pip

Python 生态最强大的地方就是海量的第三方包。安装：

```bash
pip install requests    # HTTP 请求库
pip install pandas      # 数据分析
pip install openpyxl    # 读写 Excel
```

### 项目依赖管理：requirements.txt

```
# requirements.txt
requests>=2.28.0
pandas==2.0.3
openpyxl
```

```bash
pip install -r requirements.txt   # 一次性装好所有依赖
```

---

## 9.6 虚拟环境：解决版本冲突

不同项目可能需要不同版本的同一个包。虚拟环境让每个项目有自己独立的 Python 和包。

```bash
# 创建虚拟环境
python -m venv myenv

# 激活（Linux/Mac）
source myenv/bin/activate

# 激活（Windows）
myenv\Scripts\activate

# 退出
deactivate
```

激活后，`pip install` 装的东西只会影响当前项目，不影响系统 Python。

---

## 📝 本章练习

1. 把你前面章节写的函数整理到一个 `utils.py` 模块里，在另一个文件中导入并使用。
2. 用 `pathlib` 写一个函数，递归列出某目录下所有 `.py` 文件。
3. 创建一个虚拟环境，在里面安装 `requests`，写一个脚本验证安装成功。

---

🎉 **恭喜！你完成了第二阶段！**

现在你可以：
- 用列表/字典/集合高效组织数据
- 读写文件让数据持久化
- 处理异常让程序不崩溃
- 用模块和包组织代码结构

下一步是**真正能干活了**——网络请求、数据处理、自动化脚本。

👉 进入第三阶段：[**网络请求**](../stage-03-applications/10-web-requests.md)
