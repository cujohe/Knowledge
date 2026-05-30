# 第十二章：自动化脚本

## 12.1 自动化的本质

程序能替你做的所有事情，都遵循这个模式：

```
触发器（什么时候做） → 执行（做什么） → 结果（输出/通知）
```

| 触发器 | 执行 | 结果 |
|--------|------|------|
| 每天上午 9 点 | 生成昨天的销售报表 | 发到邮箱 |
| 文件被修改时 | 备份到另一个目录 | 日志记录 |
| 收到新邮件时 | 解析附件 Excel | 存入数据库 |

---

## 12.2 实战①：自动备份脚本

```python
#!/usr/bin/env python3
"""自动备份指定目录到备份文件夹，按日期归档"""

import shutil
import datetime
from pathlib import Path

def backup(source_dir, backup_base):
    source = Path(source_dir)
    backup_dir = Path(backup_base) / f"backup_{datetime.date.today()}"
    
    if not source.exists():
        print(f"❌ 源目录不存在：{source}")
        return
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 zip 压缩包
    archive_name = backup_dir / f"{source.name}.zip"
    shutil.make_archive(
        str(archive_name.with_suffix("")),  # 不加 .zip
        "zip",                              # 格式
        source                              # 源目录
    )
    
    print(f"✅ 备份完成：{archive_name}")
    print(f"   大小：{archive_name.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    backup("~/Documents/重要文件", "~/backups")
```

---

## 12.3 实战②：批量重命名文件

```python
"""把指定目录下所有文件的文件名统一格式"""

from pathlib import Path

def batch_rename(directory, prefix="file", start_num=1, dry_run=True):
    """
    批量重命名：file_001.ext, file_002.ext ...
    dry_run=True 时只预览，不实际修改
    """
    dir_path = Path(directory).expanduser()
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    
    for i, filepath in enumerate(files, start=start_num):
        new_name = f"{prefix}_{i:03d}{filepath.suffix}"
        new_path = filepath.parent / new_name
        
        if dry_run:
            print(f"{filepath.name}  →  {new_name}")
        else:
            filepath.rename(new_path)
            print(f"✅ {new_name}")
    
    if dry_run:
        print(f"\n以上是预览（共 {len(files)} 个文件），加 --execute 执行")

if __name__ == "__main__":
    import sys
    execute = "--execute" in sys.argv
    batch_rename("~/Desktop/photos", prefix="photo", dry_run=not execute)
```

---

## 12.4 实战③：监控文件夹变化

```python
"""监控目录，有新文件时自动处理"""

import time
from pathlib import Path

def watch_folder(folder_path, callback, interval=5):
    """
    监控文件夹，每 interval 秒检查一次
    callback 是发现新文件时要执行的函数
    """
    folder = Path(folder_path).expanduser()
    known_files = set(folder.iterdir()) if folder.exists() else set()
    
    print(f"👀 正在监控：{folder}")
    
    while True:
        time.sleep(interval)
        
        if not folder.exists():
            continue
        
        current_files = set(folder.iterdir())
        new_files = current_files - known_files
        
        for new_file in new_files:
            print(f"\n📄 发现新文件：{new_file.name}")
            callback(new_file)
        
        known_files = current_files

# 使用示例
def print_file_info(filepath):
    print(f"   路径：{filepath}")
    print(f"   大小：{filepath.stat().st_size} 字节")

# watch_folder("~/Downloads", print_file_info)
```

---

## 12.5 实战④：命令行参数工具

用 `argparse` 把脚本变成专业的命令行工具：

```python
"""图片批量压缩工具"""

import argparse
from pathlib import Path

def compress_images(input_dir, output_dir, quality=85, max_width=None):
    """
    压缩目录下的所有图片
    需要安装：pip install Pillow
    """
    from PIL import Image
    
    input_path = Path(input_dir).expanduser()
    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)
    
    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    images = [f for f in input_path.iterdir() if f.suffix.lower() in extensions]
    
    for i, img_path in enumerate(images, 1):
        img = Image.open(img_path)
        original_size = img_path.stat().st_size
        
        # 等比缩放
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        out_path = output_path / img_path.name
        img.save(out_path, quality=quality, optimize=True)
        
        new_size = out_path.stat().st_size
        saved = (1 - new_size / original_size) * 100
        print(f"[{i}/{len(images)}] {img_path.name}  ({saved:.0f}% 减小)")

def main():
    parser = argparse.ArgumentParser(description="图片批量压缩工具")
    parser.add_argument("input", help="输入目录")
    parser.add_argument("-o", "--output", default="./compressed", help="输出目录")
    parser.add_argument("-q", "--quality", type=int, default=85, help="压缩质量 (1-100)")
    parser.add_argument("-w", "--max-width", type=int, help="最大宽度")
    
    args = parser.parse_args()
    compress_images(args.input, args.output, args.quality, args.max_width)

if __name__ == "__main__":
    main()
```

使用：
```bash
python compress.py ~/Pictures -o ~/compressed -q 80 -w 1920
```

---

## 12.6 实战⑤：定时任务（Crontab）

在 Linux/Mac 上，你可以用 crontab 让脚本定时执行：

```bash
# 编辑 crontab
crontab -e

# 每天上午 9 点执行备份脚本
0 9 * * * python ~/scripts/backup.py

# 每周一上午 8 点生成报表
0 8 * * 1 python ~/scripts/report.py >> ~/logs/report.log 2>&1
```

Windows 使用「任务计划程序」，或者用 Python 的 `schedule` 库：

```python
import schedule
import time

def job():
    print("执行定时任务...")

schedule.every().day.at("09:00").do(job)
schedule.every().monday.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 12.7 自动化脚本模板

```python
#!/usr/bin/env python3
"""
脚本名称：xxx
用途：xxx
使用：python xxx.py [参数]
"""

import argparse
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("script.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="脚本描述")
    parser.add_argument("input", help="输入文件/目录")
    parser.add_argument("-o", "--output", default="output", help="输出目录")
    args = parser.parse_args()
    
    logger.info("脚本开始执行")
    
    try:
        # 核心逻辑
        logger.info(f"处理：{args.input}")
        # ...
        logger.info("完成！")
    except Exception as e:
        logger.error(f"出错：{e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
```

---

## 📝 本章练习

1. 写一个脚本，遍历指定目录，把所有 `.txt` 文件合并成一个文件。
2. 写一个脚本，接收一个 URL 列表文件，依次下载每个 URL 的内容并保存。
3. 把之前写的天气查询工具改成命令行工具，接收城市名作为参数。

---

🎉 **恭喜！你完成了第三阶段！**

现在你可以：
- 发起 HTTP 请求获取网络数据
- 用 pandas 处理和分析数据
- 写自动化脚本提升工作效率

最后一步是**工程思维**——让你的代码经得起考验。

👉 进入第四阶段：[**测试**](../stage-04-engineering/13-testing.md)
