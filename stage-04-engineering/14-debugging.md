# 第十四章：调试

## 14.1 调试的本质

调试不是「找 bug」——是**验证并修正你对代码行为的假设**。

```
你心里想的：「这行代码应该输出 5」
实际发生的：「输出了 None」
调试 = 搞清楚为什么你的假设错了
```

---

## 14.2 print 调试法（最简单的，也最常用）

```python
def calculate_discount(price, discount_rate):
    print(f"[DEBUG] price={price}, rate={discount_rate}")  # 看看输入
    discounted = price * (1 - discount_rate)
    print(f"[DEBUG] discounted={discounted}")
    return discounted

result = calculate_discount(100, 0.2)
print(f"结果：{result}")
```

> 💡 对于快速定位问题，`print()` 往往足够了。但调试完记得删掉，或者用 logging 替代。

---

## 14.3 f-string 调试（Python 3.8+）

```python
# 原来要这样写
print(f"price={price}, rate={discount_rate}")

# 可以简化为（注意等号）
print(f"{price=}, {discount_rate=}")
# 输出：price=100, discount_rate=0.2
```

更绝的：

```python
x = 10
y = 20
print(f"{x + y = }")      # x + y = 30
print(f"{x * y / 2 = }")  # x * y / 2 = 100.0
```

---

## 14.4 logging：正式版的 print

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def process_order(order_id, items):
    logging.debug(f"开始处理订单 {order_id}，商品数：{len(items)}")
    
    total = 0
    for i, item in enumerate(items):
        logging.debug(f"  处理第 {i} 个商品：{item}")
        total += item.get("price", 0) * item.get("qty", 1)
    
    logging.info(f"订单 {order_id} 总额：{total}")
    return total
```

| 级别 | 用途 | 
|------|------|
| `DEBUG` | 详细调试信息（开发时开，上线后关） |
| `INFO` | 重要事件（上线后保留） |
| `WARNING` | 非预期但可处理的情况 |
| `ERROR` | 出了错误但程序还能跑 |
| `CRITICAL` | 程序可能要崩 |

---

## 14.5 专业调试：pdb 和 breakpoint()

Python 内置了一个**交互式调试器**，让你可以在代码任意位置「暂停」并检查状态。

```python
def find_bug(data):
    result = []
    for item in data:
        processed = item * 2 + 1
        breakpoint()  # ← 程序在这里暂停！
        result.append(processed)
    return result
```

当程序跑到 `breakpoint()` 时，你进入了一个交互环境：

```
(Pdb) item           # 查看 item 的值
5
(Pdb) processed      # 查看 processed 的值
11
(Pdb) type(item)     # 查看类型
<class 'int'>
(Pdb) result         # 查看当前结果列表
[]
(Pdb) c              # continue，继续执行到下一个 breakpoint
(Pdb) q              # quit，退出
```

---

### pdb 常用命令

| 命令 | 作用 |
|------|------|
| `n` (next) | 执行下一行 |
| `s` (step) | 进入函数内部 |
| `c` (continue) | 继续执行 |
| `l` (list) | 显示当前代码周围 |
| `p 变量` | 打印变量值 |
| `pp 变量` | 漂亮格式化打印 |
| `w` (where) | 显示调用栈 |
| `q` (quit) | 退出 |

---

## 14.6 实战调试流程

遇到 bug 时，按这个顺序走：

```
1. 看错误信息（Traceback）
   ↓
   最后一行的错误类型是什么？（ValueError? KeyError? AttributeError?）
   倒数第二行是哪个文件、第几行出错的？
   ↓
2. 定位到那一行
   ↓
   在出错行前面加 breakpoint()
   重新运行程序
   在 pdb 中检查每个变量的值
   ↓
3. 验证假设
   ↓
   我以为变量是 X 类型，实际是什么类型？
   我以为字典有 "key" 字段，实际有什么？
   我以为列表有 10 个元素，实际有几个？
   ↓
4. 修复
   ↓
   修好代码后，把 breakpoint() 删掉
```

---

## 14.7 常见错误速查

| 错误 | 含义 | 常见原因 |
|------|------|---------|
| `NameError` | 变量名不存在 | 拼写错误、作用域问题、变量还没赋值 |
| `TypeError` | 类型不匹配 | `"hello" + 1` 字符串和数字混用 |
| `ValueError` | 值不合法 | `int("abc")` 不能转换 |
| `KeyError` | 字典 key 不存在 | `dict["missing_key"]` |
| `IndexError` | 列表下标越界 | `list[10]` 但只有 5 个元素 |
| `AttributeError` | 对象没有这个方法 | `"hello".append()` 字符串没有 append |
| `IndentationError` | 缩进错误 | Tab 和空格混用 |
| `ImportError` | 模块不存在 | 包没装、路径不对 |

---

## 14.8 VS Code 调试

如果你用 VS Code，可以不用命令行 pdb：

1. 在代码行号左边点击 → 出现红点（断点）
2. 按 F5 启动调试
3. 程序在断点处暂停
4. 左侧面板查看所有变量值
5. F10 逐行执行，F11 进入函数
6. Shift+F5 停止

> ✅ 图形化调试比命令行直观得多，**推荐新手首选 VS Code 调试**。

---

## 📝 本章练习

1. 故意写一个有 bug 的程序（比如索引越界、除以零），用 `breakpoint()` 调试找到问题。
2. 把你之前写的某个脚本加上 logging，输出不同级别的日志。
3. 练习 VS Code 的断点调试：设置断点、查看变量、单步执行。

---

👉 下一章：[**Git 基础**](15-git-basics.md) —— 代码的时光机
