# 第六章：列表、字典、集合

## 6.1 列表（list）：有序的数据容器

列表是 Python 里最常用的数据结构。它是一串有序的值，可以随时增删改。

```python
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print(fruits[0])       # 苹果
print(fruits[-1])      # 葡萄
print(len(fruits))     # 4
```

### 6.1.1 列表操作清单

```python
nums = [1, 2, 3]

# 增
nums.append(4)         # [1, 2, 3, 4] — 加到末尾
nums.insert(0, 0)      # [0, 1, 2, 3, 4] — 在位置 0 插入
nums.extend([5, 6])    # [0, 1, 2, 3, 4, 5, 6] — 合并另一个列表

# 删
nums.pop()             # 弹出最后一个（返回 6），列表变 [0,1,2,3,4,5]
nums.pop(0)            # 弹出位置 0（返回 0），列表变 [1,2,3,4,5]
nums.remove(3)         # 移除值为 3 的元素，变 [1,2,4,5]
del nums[2]            # 删除下标 2，变 [1,2,5]

# 查
nums.index(5)          # 2 — 5 的下标
nums.count(2)          # 1 — 2 出现了 1 次
3 in nums              # True — 3 在列表里吗？

# 排序
nums.sort()            # 原地排序 [1,2,5]
sorted(nums)           # 返回新排序列表，原列表不变
nums.sort(reverse=True)# 降序 [5,2,1]
```

### 6.1.2 列表底层原理

列表在 C 层面是一个**动态数组**：

```
内存： [1][2][3][4][_][_][_][_]  ← 预分配了 8 个槽位
                       ↑
                 4 个在用，4 个空的

当你 append(5) 时：
内存： [1][2][3][4][5][_][_][_]

当槽位用满时，Python 分配一块更大的内存（通常是 1.125 倍），
把数据拷贝过去，释放旧内存。
```

> 💡 **append 的均摊时间复杂度是 O(1)**——大部分时候很快（有空槽），偶尔慢一次（需要扩容复制）。但 `insert(0, x)` 永远是 O(n)，因为要把后面所有元素往后挪。

---

### 6.1.3 列表推导式（List Comprehension）

这是 Python 最具特色的语法之一。把它用好，你的代码会从 5 行变 1 行。

```python
# 传统写法
squares = []
for i in range(10):
    squares.append(i ** 2)

# 推导式写法
squares = [i ** 2 for i in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 加条件过滤
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
# [0, 4, 16, 36, 64]

# 嵌套
pairs = [(x, y) for x in range(3) for y in range(3)]
# [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
```

---

## 6.2 元组（tuple）：不可变的列表

```python
point = (3, 4)       # 元组用圆括号
x, y = point         # 解包
print(x, y)          # 3 4

point[0] = 5         # TypeError! 元组不能修改
```

元组适合表示「固定结构的数据」——比如坐标、RGB 颜色值。因为它不可变，Python 可以优化存储，而且可以用作字典的键。

---

## 6.3 字典（dict）：键值对的王者

字典是你未来最常用的数据结构。它通过**键（key）**快速查找对应的**值（value）**。

```python
user = {
    "name": "小明",
    "age": 25,
    "city": "北京"
}

print(user["name"])     # 小明
print(user.get("phone", "无"))  # 无（key 不存在时返默认值，不报错）

# 增改
user["phone"] = "12345"       # 新增
user["age"] = 26              # 修改

# 删
del user["city"]

# 遍历
for key in user:
    print(key, user[key])

for key, value in user.items():   # 同时拿到键和值
    print(f"{key}: {value}")
```

### 6.3.1 字典底层原理：哈希表

字典之所以快（查找 O(1)），靠的是**哈希表**：

```
1. Python 对键 "name" 做 hash，得到数字 8237492
2. 把 8237492 映射到哈希表的一个槽位
3. 在槽位里存 ["name", "小明"]
4. 下次查 "name"，再算一次 hash，直接跳到对应槽位
```

> 💡 字典的键必须是**可哈希的**（不可变类型）：str、int、tuple 可以，list 不行。

---

## 6.4 集合（set）：去重 + 数学运算

```python
# 自动去重
nums = {1, 2, 2, 3, 3, 3}
print(nums)  # {1, 2, 3}

# 集合运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # {1,2,3,4,5,6} — 并集
print(a & b)   # {3,4}           — 交集
print(a - b)   # {1,2}           — 差集
print(a ^ b)   # {1,2,5,6}       — 对称差集
```

判断重复元素的神器：

```python
items = [1, 2, 3, 2, 4, 1]
duplicates = len(items) != len(set(items))  # True — 有重复
```

---

## 6.5 选择合适的数据结构

| 需求 | 用什么 | 
|------|--------|
| 有序，需要索引访问 | `list` |
| 不可变的固定数据 | `tuple` |
| 按键快速查找 | `dict` |
| 去重 + 集合运算 | `set` |
| 需要先进先出 | `collections.deque` |
| 需要计数 | `collections.Counter` |

---

## 6.6 实战：统计一段文本的词频

```python
text = """
Python is great. Python is easy to learn. 
Learn Python today. Python, Python, Python!
"""

# 简单的分词：按空格和标点拆
import re
words = re.findall(r'\b\w+\b', text.lower())

# 统计出现次数
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# 排序输出
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
for word, count in sorted_words:
    print(f"{word}: {count}")
```

输出：
```
python: 6
is: 2
learn: 2
great: 1
easy: 1
to: 1
today: 1
```

### 这里出现了 `lambda`——这是什么？

```python
lambda x: x[1]
```

等价于：

```python
def get_count(item):
    return item[1]
```

lambda 就是一个**没有名字的迷你函数**。用于「我只需要用一次」的场景。这里的 `sorted(..., key=lambda x: x[1])` 意思是「按每对的第 1 个元素（数量）排序」。

---

## 📝 本章练习

1. 用列表推导式写出 1-100 中所有能被 3 或 5 整除的数的列表。
2. 给定一个字典 `{"a": 1, "b": 2, "c": 1}`，写代码找出所有值为 1 的键。
3. 写一个函数，接收一个列表，返回「去重后排序」的新列表。

---

👉 下一章：[**文件读写**](07-file-io.md) —— 让数据持久化
