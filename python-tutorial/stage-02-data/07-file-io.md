# 第七章：文件读写

## 7.1 为什么需要文件

到目前为止，你程序里所有的数据都活在内存里——程序一关，什么都没了。文件让你能把数据**持久化**到硬盘上。

---

## 7.2 打开 → 操作 → 关闭

```python
# 经典写法
f = open("hello.txt", "w", encoding="utf-8")
f.write("Hello, World!\n")
f.write("第二行内容")
f.close()     # 必须关！否则数据可能没真正写入
```

### 更推荐的写法（自动关闭）

```python
# with 语句会在离开代码块时自动调用 close()
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行内容")
# 这里 f 已经自动关闭了
```

> 💡 **永远用 `with ... as ...`，忘了 close 是新手最常见的 bug 之一。**

---

## 7.3 文件模式（mode）速查

| 模式 | 含义 | 文件不存在时 | 文件存在时 |
|------|------|------------|-----------|
| `'r'` | 只读（默认） | 报错 | 从头读 |
| `'w'` | 只写 | 创建新文件 | **清空原内容** |
| `'a'` | 追加 | 创建新文件 | 在末尾追加 |
| `'r+'` | 读写 | 报错 | 从头操作 |
| `'x'` | 创建且只写 | 创建新文件 | 报错（防止覆盖） |

加 `b` 表示二进制模式：`'rb'`、`'wb'`（用于图片、视频等）。

---

## 7.4 读取文件

### 一次读全部

```python
with open("hello.txt", "r", encoding="utf-8") as f:
    content = f.read()       # 整个文件读成一个字符串
    print(content)
```

### 逐行读（大文件用这个）

```python
with open("hello.txt", "r", encoding="utf-8") as f:
    for line in f:           # 一次只读一行到内存
        print(line.strip())  # strip() 去掉行尾的换行符
```

### 读成列表

```python
with open("hello.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()    # 每行一个元素
    print(lines)
```

---

### 7.4.1 `encoding='utf-8'` 是什么

它是字符编码。简单理解：计算机只存数字，要存文字就得把文字映射到数字。UTF-8 是当今最通用的映射方案，能表示中文、英文、emoji 等几乎所有字符。

省略 encoding 时 Python 用系统默认编码——Windows 上可能是 GBK，Linux/Mac 是 UTF-8。**跨平台时经常因此出现乱码**。所以**永远显式写 `encoding='utf-8'`**。

---

## 7.5 实战①：写一个简单的日记本

```python
import datetime

def write_diary():
    """在文件末尾追加一篇日记"""
    content = input("今天想写点什么？\n> ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    with open("diary.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {timestamp} ---\n")
        f.write(f"{content}\n")
    
    print("已保存！")

def read_diary():
    """读取所有日记"""
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("还没有写过日记呢。")

def main():
    while True:
        cmd = input("日记本 [w=写, r=读, q=退出]: ")
        if cmd == 'w':
            write_diary()
        elif cmd == 'r':
            read_diary()
        elif cmd == 'q':
            break

if __name__ == "__main__":
    main()
```

---

### 7.5.1 `if __name__ == "__main__"` 是什么

```python
# diary.py
def main():
    print("我是日记本")

if __name__ == "__main__":
    main()
```

当你 `python diary.py` 时，Python 把 `__name__` 设为 `"__main__"`，所以 `main()` 会执行。

当别的文件 `import diary` 时，`__name__` 是 `"diary"`，所以 `main()` 不执行——你只是导入了它的函数，没有运行程序。

> 💡 **这是 Python 模块化的基础**：每个 `.py` 文件既可以当独立程序运行，也可以当库被导入。

---

## 7.6 实战②：CSV 文件处理

CSV（逗号分隔值）是数据交换中最常见的格式。Python 自带 `csv` 模块。

```python
import csv

# 写入 CSV
data = [
    ["姓名", "年龄", "城市"],
    ["张三", 25, "北京"],
    ["李四", 30, "上海"],
    ["王五", 28, "广州"],
]

with open("users.csv", "w", newline="", encoding="utf-8-sig") as f:
    # utf-8-sig：加 BOM，让 Excel 正确识别中文
    writer = csv.writer(f)
    writer.writerows(data)

print("已写入 users.csv")
```

```python
# 读取 CSV
with open("users.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)  # 第一行自动当表头
    for row in reader:
        print(f"{row['姓名']}, {row['年龄']}岁, 住在{row['城市']}")
```

输出：
```
张三, 25岁, 住在北京
李四, 30岁, 住在上海
王五, 28岁, 住在广州
```

---

## 7.7 JSON 文件

JSON 是互联网数据交换的事实标准。Python 的处理极简：

```python
import json

user = {
    "name": "小明",
    "age": 25,
    "hobbies": ["编程", "跑步"],
    "married": False
}

# 写入 JSON
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False: 让中文正常显示
    # indent=2: 缩进，好看

# 读取 JSON
with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(data["name"])  # 小明
```

---

## 📝 本章练习

1. 写一个「待办事项」程序：从 `todo.txt` 读取任务列表，支持添加（a）、查看（v）、标记完成并删除（d）。
2. 读一个 CSV 文件，计算某一列的平均值。
3. 把第六章的词频统计程序改成从文件读入，结果输出到另一个文件。

---

👉 下一章：[**异常处理**](08-error-handling.md) —— 程序崩了怎么办
