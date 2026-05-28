# 04_数据存储与交互（SQLite）：将数据持久化

在上一章中，我们已经使用 Flask 实现了 RESTful API 的骨架，并初步运行了应用。尽管我们使用了 `db.create_all()`，但现在并没有明确的数据持久化存储，因为 Flask-SQLAlchemy 的集成还不完整。本章我们将深入探讨如何使用 SQLite 数据库配合 SQLAlchemy 来实现数据的持久化存储和管理。

## 1. 数据库基础：为什么需要数据库？

在没有数据库之前，我们的 API 如果每次重启，之前创建的任务数据就会丢失。这是因为数据只存在于内存中，当程序关闭时，内存会被清空。

**数据库 (Database)** 就是用来解决数据持久化问题的。它是一个结构化的数据集合，可以长期存储和管理数据。当程序需要数据时，从数据库中读取；当数据发生变化时，写入数据库。

### 关系型数据库 (Relational Database)

我们选择的 SQLite 属于关系型数据库。关系型数据库的核心概念是：
*   **表 (Table)**：数据以表格的形式组织，类似于 Excel 表格，有行和列。
*   **行 (Row) / 记录 (Record)**：表中的每一行代表一个独立的实体 (例如，一个任务)。
*   **列 (Column) / 字段 (Field)**：表中的每一列代表实体的一个属性 (例如，任务的标题、描述)。
*   **主键 (Primary Key)**：唯一标识表中每一行记录的列 (例如，任务的 `id`)。
*   **SQL (Structured Query Language)**：用于与关系型数据库进行交互的标准语言，可以进行数据的查询、插入、更新和删除。

### 为什么选择 SQLite？

*   **轻量级，无需独立服务器**：SQLite 是一个嵌入式数据库，它不是一个独立的服务器进程，而是直接集成在应用程序中。数据存储在一个文件中 (通常是 `.db` 或 `.sqlite` 后缀)。
*   **零配置，易于使用**：无需复杂的安装和配置，非常适合开发、测试和小型应用。
*   **跨平台**：在所有操作系统上都能正常工作。

## 2. ORM (Object-Relational Mapper) 概念

直接使用 SQL 语句来操作数据库虽然灵活，但在 Python 代码中频繁地拼接 SQL 字符串会：
*   **繁琐且易错**：需要手动处理字符串转义、类型转换等。
*   **可读性差**：SQL 语句和 Python 代码混杂，难以阅读。
*   **与数据库绑定紧密**：切换数据库类型可能需要修改大量 SQL 语句。

**ORM (Object-Relational Mapper)** 是一种编程技术，它在面向对象语言和关系型数据库之间提供了一个抽象层。通过 ORM，你可以使用面向对象的方式 (Python 类和对象) 来操作数据库，而无需直接编写 SQL 语句。

**通俗比喻**：ORM 就像一个“翻译官”，它把你写的 Python 代码“翻译”成 SQL 语句去和数据库沟通，再把数据库返回的结果“翻译”成 Python 对象返回给你。

### SQLAlchemy：Python 最强大的 ORM

**SQLAlchemy** 是 Python 中最强大的 ORM 工具之一，它提供了完整的 ORM 功能，也可以只用作 SQL 工具包。`Flask-SQLAlchemy` 是 Flask 的一个扩展，它封装了 SQLAlchemy，使得在 Flask 应用中集成和使用 SQLAlchemy 变得非常简单。

## 3. `models.py`：定义数据库模型

我们在第一章中已经初步定义了 `models.py`。现在，我们来详细解读它，并确认它与数据库的映射关系。

```python
# code/task_app/models.py
from datetime import datetime
from .app import db # 从 app 模块导入 db 实例，这个 db 是 Flask-SQLAlchemy 的实例

class Task(db.Model):
    # db.Model 是 Flask-SQLAlchemy 提供的基类，Task 类继承它表示这是一个数据库模型

    id = db.Column(db.Integer, primary_key=True) # 主键，整数类型，自动增长
    title = db.Column(db.String(100), nullable=False) # 字符串类型，最大长度 100，不允许为空
    description = db.Column(db.String(200), nullable=True) # 字符串类型，最大长度 200，允许为空
    status = db.Column(db.String(50), default='pending') # 字符串类型，默认值为 'pending'
    due_date = db.Column(db.String(10), nullable=True) # 字符串类型，用于存储 YYYY-MM-DD 格式的日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # 创建时间，默认是 UTC 当前时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # 更新时间，每次更新时自动更新为 UTC 当前时间

    def __repr__(self): # 定义对象的字符串表示，方便调试
        return f'<Task {self.id}: {self.title}>'

    def to_dict(self): # 将 Task 对象转换为字典，方便 JSON 序列化
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'due_date': self.due_date,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
```

**关键点解析：**
*   `db.Model`：`Task` 类通过继承 `db.Model` 成为一个 SQLAlchemy 模型。这个模型将映射到数据库中的一个表，默认情况下表名就是类名的小写 (即 `task`)。
*   `db.Column`：用于定义表的列。每个属性 (如 `id`, `title`) 都对应数据库表中的一列。
    *   `db.Integer`, `db.String`, `db.DateTime`：这些是 SQLAlchemy 提供的列类型，它们会根据你使用的数据库类型 (SQLite, PostgreSQL, MySQL 等) 自动映射到合适的数据库类型。
    *   `primary_key=True`：将 `id` 列设为主键。对于 SQLite，整数主键会自动设置为 `AUTOINCREMENT`。
    *   `nullable=False`：表示该列不能存储 `NULL` 值。
    *   `default=datetime.utcnow`：设置列的默认值。`datetime.utcnow` 是一个函数，每次创建新记录时，都会调用它来获取当前 UTC 时间。
    *   `onupdate=datetime.utcnow`：当记录更新时，`updated_at` 列会自动更新为当前的 UTC 时间。
*   `__repr__` 方法：在调试时非常有用，当你打印一个 `Task` 对象时，它会显示一个更具可读性的字符串表示。
*   `to_dict()` 方法：这是我们自定义的一个辅助方法。API 通常返回 JSON 格式的数据，通过这个方法，我们可以方便地将 `Task` 实例转换为 Python 字典，然后 `jsonify()` 可以将其转换为 JSON 字符串。

## 4. `app.py` 中的数据库初始化

在 `code/task_app/app.py` 中，我们已经包含了数据库的初始化代码：

```python
# code/task_app/app.py 节选
...
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # !!! 关键一步 !!!
    with app.app_context():
        db.create_all() # 在应用上下文内创建所有数据库表

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Task Management API!"})

    return app
...
```

**`db.create_all()` 的作用：**
这个方法会根据 `db.Model` 注册的所有模型 (`Task` 模型)，在数据库中创建相应的表。如果表已经存在，它会跳过创建。在开发和测试阶段，这非常方便。然而，在生产环境中，当你的数据库模型发生变化时，直接运行 `create_all()` 可能会导致数据丢失或表结构不匹配。因此，生产环境通常使用数据库迁移工具 (如 Alembic) 来安全地管理数据库结构变化。

**`with app.app_context():`**：
`db.create_all()` 需要在 Flask 应用上下文 (Application Context) 中运行，因为它需要访问应用的配置 (`app.config`) 和数据库实例 (`db`)。`with app.app_context():` 确保了代码在正确的上下文中执行。

## 5. `routes.py` 中的数据库交互

在 `code/task_app/routes.py` 中，我们已经使用了 SQLAlchemy 来进行数据库的增删改查操作。

**查询数据：**
*   `Task.query.all()`：查询 `task` 表中的所有记录，并返回 `Task` 对象列表。
*   `Task.query.get_or_404(task_id)`：根据主键 `task_id` 查询单个 `Task` 记录。如果找到了，返回 `Task` 对象；如果没找到，会自动返回一个 404 Not Found 错误响应。

**新增数据：**
```python
# routes.py 节选
...
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'pending'),
        due_date=data.get('due_date')
    )
    db.session.add(new_task) # 将新创建的 Task 对象添加到数据库会话中
    db.session.commit()      # 提交会话，将数据写入数据库
...
```
*   `db.session.add(new_task)`：将 `new_task` 对象添加到当前数据库会话中。这相当于告诉 SQLAlchemy：“我想要将这个对象保存到数据库。”
*   `db.session.commit()`：提交当前会话中的所有更改 (包括 `add`, `update`, `delete` 等操作) 到数据库。这是实际执行数据库写入操作的关键一步。

**更新数据：**
```python
# routes.py 节选
...
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.due_date = data.get('due_date', task.due_date)

    db.session.commit() # 提交会话，更新数据库中的记录
...
```
*   当你修改一个从数据库中获取的 `Task` 对象的属性时，SQLAlchemy 会自动追踪这些变化。你只需要再次调用 `db.session.commit()`，它就会将这些变化保存到数据库中。

**删除数据：**
```python
# routes.py 节选
...
    db.session.delete(task) # 从数据库会话中删除 Task 对象
    db.session.commit()     # 提交会话，从数据库中删除记录
...
```
*   `db.session.delete(task)`：将 `task` 对象标记为待删除。
*   `db.session.commit()`：执行删除操作。

## 6. 重新运行并验证数据库持久化

现在，你可以再次按照第 03 章末尾的步骤运行 `app.py`。

1.  **启动应用**：`python app.py`
2.  **创建几个任务**：使用 `POST /tasks` 创建任务。
3.  **停止应用**：`CTRL+C` 停止服务器。
4.  **再次启动应用**：`python app.py`
5.  **获取所有任务**：`curl http://127.0.0.1:5000/tasks`

你会发现之前创建的任务数据依然存在！这意味着你的数据已经被成功持久化到 `instance/tasks.db` 文件中。

### 数据库文件位置

在 `code/task_app/` 目录下，你会看到一个名为 `instance/tasks.db` 的文件 (或者 `instance/` 目录)。这就是你的 SQLite 数据库文件。

由于我们在 `.gitignore` 中忽略了 `instance/` 和 `*.db`，所以这个数据库文件不会被 Git 追踪，这非常重要，因为它通常只与本地开发环境相关。

至此，我们已经成功地将数据库集成到 Flask 应用中，并实现了数据的持久化。下一章，我们将讨论如何为这个 API 编写自动化测试，以确保代码的质量和功能的正确性。
