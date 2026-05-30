# 第十一章：数据处理

## 11.1 Python vs Excel

| 场景 | Excel | Python |
|------|-------|--------|
| 几百行数据，做个图表 | ✅ 适合 | 杀鸡用牛刀 |
| 几万行数据，多表关联 | 卡到崩溃 | ✅ 秒出结果 |
| 每个月做同样的报表 | 手动操作 | ✅ 脚本一次写完，月月自动跑 |
| 数据来源是 API/数据库 | 不好搞 | ✅ 直接读 |

> 💡 **Python 不是要替代 Excel，而是做 Excel 做不了的事儿。**

---

## 11.2 pandas：数据分析的瑞士军刀

```bash
pip install pandas openpyxl
```

pandas 的核心概念就两个：

- **Series**：一列数据（带行标签）
- **DataFrame**：一张表（多列 Series 拼在一起）

```python
import pandas as pd

# 从字典创建 DataFrame
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [25, 30, 28, 35],
    "城市": ["北京", "上海", "广州", "深圳"],
    "工资": [15000, 20000, 18000, 25000]
}

df = pd.DataFrame(data)
print(df)
```

```
   姓名  年龄  城市    工资
0  张三  25  北京  15000
1  李四  30  上海  20000
2  王五  28  广州  18000
3  赵六  35  深圳  25000
```

---

## 11.3 DataFrame 基本操作

```python
# 查看基本信息
df.head(2)           # 前两行
df.shape             # (4, 4) — 4 行 4 列
df.info()            # 每列的数据类型和非空数量
df.describe()        # 数值列的统计摘要（均值、标准差等）

# 选择列
df["姓名"]           # 返回 Series
df[["姓名", "工资"]]  # 返回 DataFrame（多列）

# 筛选行
df[df["年龄"] > 28]              # 年龄大于 28 的
df[df["城市"] == "北京"]          # 北京的员工
df[(df["年龄"] > 25) & (df["工资"] > 18000)]  # 两个条件

# 排序
df.sort_values("工资", ascending=False)  # 按工资降序

# 新增列
df["年薪"] = df["工资"] * 12
df["高薪"] = df["工资"] > 18000  # 自动变成布尔列
```

---

## 11.4 实战①：从 Excel 读取，处理后写回

假设有一个 `sales.xlsx`：

| 日期 | 产品 | 数量 | 单价 |
|------|------|------|------|
| 2024-01-01 | A | 10 | 100 |
| 2024-01-02 | B | 5 | 200 |
| ... | ... | ... | ... |

```python
import pandas as pd

# 读 Excel
df = pd.read_excel("sales.xlsx")

# 计算销售额
df["销售额"] = df["数量"] * df["单价"]

# 按产品汇总
summary = df.groupby("产品").agg(
    总销量=("数量", "sum"),
    总销售额=("销售额", "sum"),
    平均单价=("单价", "mean")
).reset_index()

# 加一行「合计」
summary.loc["合计"] = summary.select_dtypes(include="number").sum()
summary.at["合计", "产品"] = "合计"

# 写回 Excel
with pd.ExcelWriter("sales_report.xlsx") as writer:
    df.to_excel(writer, sheet_name="明细", index=False)
    summary.to_excel(writer, sheet_name="汇总", index=False)

print("报表已生成：sales_report.xlsx")
```

---

## 11.5 实战②：CSV 数据清洗

原始数据常常很脏：

```python
import pandas as pd

df = pd.read_csv("dirty_data.csv", encoding="utf-8")

print("清洗前：")
print(f"行数：{len(df)}")
print(f"重复行：{df.duplicated().sum()}")
print(f"缺失值：\n{df.isnull().sum()}")

# 去重
df = df.drop_duplicates()

# 处理缺失值
df["年龄"] = df["年龄"].fillna(df["年龄"].median())  # 用中位数填
df["城市"] = df["城市"].fillna("未知")

# 去除异常值（比如年龄不能是负数或超过 150）
df = df[(df["年龄"] > 0) & (df["年龄"] < 150)]

# 统一格式：城市名首字母大写
df["城市"] = df["城市"].str.strip().str.title()

print(f"\n清洗后行数：{len(df)}")
df.to_csv("clean_data.csv", index=False, encoding="utf-8-sig")
```

---

## 11.6 实战③：多表关联（VLOOKUP 替代）

```python
# 员工表
employees = pd.DataFrame({
    "员工ID": [1, 2, 3, 4],
    "姓名": ["张三", "李四", "王五", "赵六"],
    "部门ID": [101, 102, 101, 103]
})

# 部门表
departments = pd.DataFrame({
    "部门ID": [101, 102, 103],
    "部门名": ["技术部", "市场部", "人事部"]
})

# 关联（相当于 Excel 的 VLOOKUP）
result = employees.merge(departments, on="部门ID", how="left")
print(result)
```

```
   员工ID  姓名  部门ID  部门名
0      1  张三    101  技术部
1      2  李四    102  市场部
2      3  王五    101  技术部
3      4  赵六    103  人事部
```

`how="left"` 表示以左表（employees）为准。其他选项：`"inner"`（交集）、`"right"`（以右表为准）、`"outer"`（并集）。

---

## 11.7 数据可视化

```bash
pip install matplotlib
```

```python
import pandas as pd
import matplotlib.pyplot as plt

# 准备数据
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "销售额": [120, 135, 148, 162, 155, 180]
})

# 设置中文字体（Windows 用 SimHei，Mac 用 Arial Unicode MS）
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 画图
plt.figure(figsize=(10, 5))
plt.plot(df["月份"], df["销售额"], marker="o", linewidth=2)
plt.title("上半年销售额趋势")
plt.xlabel("月份")
plt.ylabel("销售额（万元）")
plt.grid(True, alpha=0.3)

# 保存
plt.savefig("sales_trend.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## 📝 本章练习

1. 创建一个 10 行 × 5 列的随机数据 DataFrame，计算每列的均值、最大值、最小值。
2. 从一个 CSV 里读入数据，筛选出符合某一条件的行，写到一个新 CSV。
3. 用 pandas 读一个 Excel，按某一列分组求和，画一个柱状图。

---

👉 下一章：[**自动化脚本**](12-automation.md) —— 让计算机替你干活
