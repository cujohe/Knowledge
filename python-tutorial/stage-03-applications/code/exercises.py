"""
第三阶段配套代码：网络请求、数据处理、自动化脚本
"""

import requests
import csv
import sys
import time
from pathlib import Path


# ============================================================
# weather.py — 天气查询
# ============================================================

def get_weather(city):
    """查询指定城市的天气"""
    url = f"https://wttr.in/{city}?format=j1&lang=zh"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]

        print(f"\n🏙️  {city}")
        print(f"🌡️  温度：{current['temp_C']}°C")
        print(f"☁️  天气：{current['weatherDesc'][0]['value']}")
        print(f"💧 湿度：{current['humidity']}%")
        print(f"🌬️  风速：{current['windspeedKmph']} km/h")

    except requests.RequestException as e:
        print(f"查询失败：{e}")


# ============================================================
# github_search.py — GitHub 仓库搜索
# ============================================================

def search_github(keyword, max_results=5):
    """搜索 GitHub 仓库"""
    url = "https://api.github.com/search/repositories"
    params = {"q": keyword, "sort": "stars", "order": "desc", "per_page": max_results}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"\n🔍 搜索 '{keyword}'（按星数排）：\n")
        for i, repo in enumerate(data["items"], 1):
            stars = repo["stargazers_count"]
            print(f"{i}. {repo['full_name']}")
            print(f"   ⭐ {stars} | {repo.get('description', '无描述')}")
            print(f"   🔗 {repo['html_url']}\n")

    except requests.RequestException as e:
        print(f"搜索失败：{e}")


# ============================================================
# data_analysis.py — 数据分析
# ============================================================

def demo_data_analysis():
    """演示 pandas 数据分析（需要 pip install pandas openpyxl）"""
    try:
        import pandas as pd
    except ImportError:
        print("请先安装：pip install pandas openpyxl")
        return

    # 创建示例数据
    df = pd.DataFrame({
        "日期": pd.date_range("2024-01-01", periods=10, freq="D"),
        "产品": ["A", "B", "A", "C", "B", "A", "C", "B", "A", "C"],
        "数量": [10, 5, 8, 12, 6, 9, 15, 7, 11, 13],
        "单价": [100, 200, 100, 150, 200, 100, 150, 200, 100, 150],
    })

    # 新增计算列
    df["销售额"] = df["数量"] * df["单价"]

    # 按产品汇总
    summary = df.groupby("产品").agg(
        总销量=("数量", "sum"),
        总销售额=("销售额", "sum"),
        平均单价=("单价", "mean"),
    ).round(2)

    print("📊 销售数据汇总：\n")
    print(summary)

    # 保存
    output = "demo_sales_report.xlsx"
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, sheet_name="明细", index=False)
        summary.reset_index().to_excel(writer, sheet_name="汇总", index=False)

    print(f"\n✅ 已保存到 {output}")


# ============================================================
# batch_rename.py — 批量重命名
# ============================================================

def batch_rename(directory, prefix="file", start_num=1, dry_run=True):
    """批量重命名文件"""
    dir_path = Path(directory).expanduser()

    if not dir_path.exists():
        print(f"❌ 目录不存在：{dir_path}")
        return

    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    print(f"📁 {dir_path}（共 {len(files)} 个文件）\n")

    for i, filepath in enumerate(files, start=start_num):
        new_name = f"{prefix}_{i:03d}{filepath.suffix}"
        new_path = filepath.parent / new_name

        if dry_run:
            print(f"  {filepath.name}  →  {new_name}")
        else:
            filepath.rename(new_path)
            print(f"  ✅ {new_name}")

    if dry_run:
        print(f"\n🔍 以上是预览。加 --execute 参数执行实际操作。")


# ============================================================
# backup.py — 自动备份
# ============================================================

def backup(source_dir, backup_base="~/backups"):
    """备份目录到 zip"""
    import shutil

    source = Path(source_dir).expanduser()
    backup_dir = Path(backup_base).expanduser()

    if not source.exists():
        print(f"❌ 源目录不存在：{source}")
        return

    backup_dir.mkdir(parents=True, exist_ok=True)

    # 按日期命名
    today = time.strftime("%Y-%m-%d")
    archive_path = backup_dir / f"{source.name}_{today}"

    shutil.make_archive(str(archive_path), "zip", source)
    print(f"✅ 备份完成：{archive_path}.zip")
    print(f"   大小：{Path(str(archive_path) + '.zip').stat().st_size / 1024:.1f} KB")


# ============================================================
# 主菜单
# ============================================================

if __name__ == "__main__":
    print("=== 第三阶段练习代码 ===\n")
    print("1. 天气查询")
    print("2. GitHub 搜索")
    print("3. 数据分析演示")
    print("4. 批量重命名（预览）")
    print("5. 备份脚本")

    choice = input("\n选择 (1-5): ")

    if choice == "1":
        city = input("城市名：")
        get_weather(city)
    elif choice == "2":
        keyword = input("搜索关键词：")
        search_github(keyword)
    elif choice == "3":
        demo_data_analysis()
    elif choice == "4":
        directory = input("目录路径：")
        prefix = input("前缀（默认 file）：") or "file"
        execute = "--execute" in sys.argv
        batch_rename(directory, prefix, dry_run=not execute)
    elif choice == "5":
        source = input("要备份的目录：")
        backup(source)
