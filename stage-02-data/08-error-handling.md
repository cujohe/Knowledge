# 第八章：异常处理

## 8.1 程序为什么会崩

```python
# 正常代码
num = int(input("输入一个数字："))
print(100 / num)
```

如果用户输入 `"abc"` 或者 `0`，程序直接崩：

```
ValueError: invalid literal for int() with base 10: 'abc'
ZeroDivisionError: division by zero
```

你不可能控制用户的行为。但你可以控制程序不崩。

---

## 8.2 try-except：给程序装安全气囊

```python
try:
    num = int(input("输入一个数字："))
    print(100 / num)
except ValueError:
    print("请输入有效的数字！")
except ZeroDivisionError:
    print("不能除以零！")
```

### 执行流程

```
1. Python 执行 try 块里的代码
2. 如果某行出错 → 跳到对应的 except 块 → 执行 except 块 → 继续执行后面代码
3. 如果没出错 → 跳过所有 except 块 → 继续执行后面代码
4. 如果错误类型不匹配任何 except → 程序仍然崩
```

---

## 8.3 捕获异常的各种写法

```python
# 捕获多种异常，统一处理
try:
    risky_operation()
except (ValueError, TypeError, KeyError):
    print("出了某种意料之中的错误")

# 捕获所有异常（不推荐，会隐藏意料之外的bug）
try:
    risky_operation()
except Exception as e:
    print(f"出错了：{e}")

# 获取错误信息
try:
    num = int("abc")
except ValueError as e:
    print(f"具体错误：{e}")   # invalid literal for int() with base 10: 'abc'
```

---

## 8.4 else 和 finally

```python
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("文件不存在")
else:
    print(f"成功读取，长度：{len(content)}")   # 仅在没出错时执行
finally:
    f.close()      # 无论出不出错，都执行（清理资源）
```

| 块 | 何时执行 |
|----|---------|
| `try` | 总是先执行 |
| `except` | try 里出错时执行 |
| `else` | try 里没出错时执行 |
| `finally` | 无论如何都执行（最后） |

---

## 8.5 实战：健壮的猜数字游戏

用异常处理加固第四章的猜数字游戏：

```python
import random

def guess_number():
    answer = random.randint(1, 100)
    attempts = 0
    
    print("猜数字游戏（1-100），输入 q 退出")
    
    while True:
        user_input = input(f"第{attempts + 1}次猜测：")
        
        if user_input.lower() == 'q':
            print(f"答案是 {answer}，下次加油！")
            break
        
        try:
            guess = int(user_input)
        except ValueError:
            print("请输入有效数字！")
            continue
        
        if guess < 1 or guess > 100:
            print("请输入 1-100 之间的数字！")
            continue
        
        attempts += 1
        
        if guess == answer:
            print(f"恭喜！答案是 {answer}，你用了 {attempts} 次。")
            break
        elif guess > answer:
            print("太大了！")
        else:
            print("太小了！")

guess_number()
```

---

## 8.6 什么时候该捕获，什么时候不该

| 场景 | 做法 | 
|------|------|
| 用户输入可能不正常 | ✅ 捕获 |
| 读文件，文件可能不存在 | ✅ 捕获 |
| 网络请求可能超时 | ✅ 捕获 |
| 你写错了变量名 | ❌ 让它崩，这是 bug 需要修 |
| 逻辑错误（应该等于 3，结果是 5） | ❌ 让它崩，你写了 bug |

> 💡 **核心原则**：捕获你能预见的、由外部因素导致的异常。不要用 try-except 掩盖你代码本身的问题。

---

## 8.7 自定义异常

```python
class InsufficientFundsError(Exception):
    """余额不足"""
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(
            f"余额 {balance} 不足，无法取出 {amount}"
        )
    return balance - amount

try:
    new_balance = withdraw(100, 200)
except InsufficientFundsError as e:
    print(e)  # 余额 100 不足，无法取出 200
```

`raise` 就是「主动抛异常」——我预判到这里可能不合理，让调用方去处理。

---

## 📝 本章练习

1. 加固第七章的日记本：用户输入文件路径时，如果路径不存在给出友好提示。
2. 写一个函数 `safe_divide(a, b)`，处理除数为 0 和非数字输入，返回结果或 None。
3. 模拟一个银行转账：转出金额大于余额时抛自定义异常，调用方捕获并给出提示。

---

👉 下一章：[**模块与包**](09-modules-packages.md) —— 如何组织你的代码
