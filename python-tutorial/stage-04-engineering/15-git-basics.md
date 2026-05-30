# 第十五章：Git 基础

## 15.1 Git 是什么

Git 是**代码的时光机**——它记录你代码的每一次修改，让你可以：

- 回到过去的任意版本
- 查看每次改了什么
- 跟别人协作不打架
- 在不同功能之间来回切换

---

## 15.2 核心概念（先建立心智模型）

```
工作区（Working Directory）     ← 你在改的文件
    ↓ git add                  ← 标记哪些修改要保存
暂存区（Staging Area）         ← 「我准备好了，要拍这张快照」
    ↓ git commit               ← 正式保存快照
仓库（Repository）             ← 所有快照的集合
```

一张图：

```
   [file.py 改了一行]       工作区
           │ git add
           ▼
   [待提交的 file.py]      暂存区
           │ git commit -m "修复了登录bug"
           ▼
   [commit #abc1234]        仓库（历史记录）
```

> 💡 **commit = 一次快照**。每次 commit 都是整个项目在那个时刻的完整状态。Git 不会存「差异」，而是存「当时的全部文件」。

---

## 15.3 Git 的底层：内容寻址文件系统

Git 的核心是一个**键值数据库**。每个文件、每个目录、每次 commit 都由一个 SHA-1 哈希值（40 位十六进制）唯一标识：

```
commit:  a1b2c3d4e5f6...  ← 这个哈希值由内容决定
tree:    0a1b2c3d4e5...   ← 目录结构的快照
blob:    f6e5d4c3b2a1...  ← 文件内容的快照（blob = binary large object）
```

```
commit a1b2c3
    ├── tree 0a1b2c    ← 根目录
    │   ├── blob f6e5d  (main.py 的内容)
    │   ├── blob a1b2c  (utils.py 的内容)
    │   └── tree 3d4e5  ← 子目录
    │       └── blob c4d5e  (helper.py 的内容)
    ├── author: "Your Name"
    ├── message: "Initial commit"
    └── parent: None    ← 指向上一个 commit
```

> 🧠 这意味着：**相同的文件内容 = 相同的 blob = 相同的哈希**。Git 不会重复存储相同内容的文件——这就是为什么 Git 在大量重复文件时不会膨胀。

---

## 15.4 基本操作

### 创建仓库

```bash
git init                    # 在当前目录初始化（通常在项目根目录）
```

### 查看状态

```bash
git status                  # 最常用的命令，时刻告诉你发生了什么
```

### 暂存和提交

```bash
git add hello.py            # 暂存单个文件
git add .                   # 暂存所有修改
git commit -m "添加了问候功能"  # 提交并写说明
```

### 查看历史

```bash
git log                     # 查看提交历史
git log --oneline           # 简洁模式
git log --oneline --graph   # 带分支图
```

### 查看改动

```bash
git diff                    # 工作区 vs 暂存区
git diff --staged           # 暂存区 vs 最新 commit
git show <commit_hash>      # 查看某次 commit 的详细改动
```

---

## 15.5 分支：并行开发的魔法

```
main ───●───●───●───●───●───
                \
feature ────────●───●───●
```

```bash
git branch feature-login    # 创建分支
git switch feature-login    # 切换到该分支（也可用 git checkout）
git switch -c feature-login # 创建并切换（一步到位）

# 开发完毕后
git switch main             # 回到 main
git merge feature-login     # 把 feature-login 的改动合入 main
git branch -d feature-login # 删掉已完成的分支
```

---

### 15.5.1 merge 的底层

当 Git merge 时：

1. 找到两个分支的**共同祖先**（分叉点那个 commit）
2. 计算从共同祖先到 A 分支的变化
3. 计算从共同祖先到 B 分支的变化
4. 尝试把两组变化合并

**Fast-forward**（快进）：如果 main 在你分叉后没动过，直接移动指针就行——不需要创建新的 merge commit。

**Three-way merge**（三方合并）：如果两边都改了，Git 创建一个新的 merge commit，整合两边的改动。

**冲突**：如果两边改了同一文件的同一行，Git 不知道怎么合并——需要你手动解决。

---

## 15.6 远程仓库（GitHub）

```bash
# 关联远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送
git push -u origin main     # 第一次推送（-u 设置上游）
git push                    # 之后直接 push 就行

# 拉取
git pull                    # 从远程拉取最新代码并合并
git fetch                   # 只看远程有没有更新，但不合并
```

---

## 15.7 日常工作流

```bash
# 每天开始工作时
git pull                    # 拉最新代码

# 开发新功能
git switch -c feature-xxx   # 新建分支
# ... 写代码 ...
git add .
git commit -m "完成了 xxx 功能"

# 推送到远程
git push -u origin feature-xxx

# 到 GitHub 上创建 Pull Request（PR）
# 同事 review 通过后，合并到 main

# 清理本地
git switch main
git pull
git branch -d feature-xxx   # 删掉本地已完成的分支
```

---

## 15.8 救命命令（日常最需要记住的）

```bash
# 「我刚才提交的信息写错了」
git commit --amend -m "新的提交信息"

# 「我改乱了，想回到上一次 commit 的状态」
git restore 文件名            # 丢弃特定文件的修改
git restore .                 # 丢弃所有修改（危险！）

# 「我已经 add 了，但不想提交了」
git restore --staged 文件名   # 从暂存区拿回工作区

# 「上次 commit 忘了加一个文件」
git add 忘记的文件
git commit --amend --no-edit  # 追加到上次 commit

# 「我搞砸了，想回到某次 commit」
git log --oneline             # 先找到目标 commit 的哈希
git switch -c recovery abc1234  # 创建一个新分支指向那个 commit
```

---

## 15.9 `.gitignore`：告诉 Git 忽略什么

在项目根目录创建 `.gitignore` 文件：

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# 编辑器
.vscode/
.idea/

# 操作系统
.DS_Store
Thumbs.db

# 项目特定
secrets.json
*.log
```

匹配规则：
- `*.pyc` — 所有 .pyc 文件
- `venv/` — venv 目录
- `!.gitkeep` — 例外（即使匹配了规则，也追踪这个文件）

---

## 📝 本章练习

1. 在当前项目目录执行 `git init`，把之前写的代码 add 并 commit。
2. 创建一个新分支，在分支上改点东西，commit，然后 merge 回 main。
3. 故意制造一个冲突（在 main 和另一个分支上改同一行），然后练习解决冲突。

---

## 🎓 教程结语

恭喜你完成了从零到工程实践的完整旅程！

回顾你走过的路：

```
程序是什么           →  理解计算机如何执行代码
变量与内存           →  理解数据如何在底层存活
数据类型             →  数字、文字、真假的处理
条件与循环           →  让程序「思考」和「重复」
函数                 →  封装逻辑，复用代码
列表/字典/集合        →  高效组织数据
文件读写             →  数据持久化
异常处理             →  让程序不崩溃
模块与包             →  组织代码结构
网络请求             →  连接互联网世界
数据处理             →  用 pandas 替代 Excel
自动化脚本           →  让计算机替你工作
测试                 →  保证代码质量
调试                 →  定位问题的侦探技巧
Git                  →  代码的时光机
```

你已经不是「会写 Python 代码」了——你理解了程序如何运行、数据如何存储、代码如何组织、质量如何保证。

**下一步建议**：
- 用学到的东西解决一个你真遇到的重复性任务
- 给开源项目提一个 Pull Request
- 学一个 Web 框架（Flask 或 FastAPI），把你的工具做成网页

编程这条路没有终点——**解决问题的能力才是你真正的武器**。🚀
