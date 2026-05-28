# 03_API 设计与实现（Flask）：构建你的第一个 RESTful API

在本章中，我们将正式开始使用 Flask 框架构建我们的任务管理 RESTful API。我们将学习 RESTful API 的核心概念，并利用 Flask 的路由、请求与响应机制，实现 API 的基本骨架。

## 1. RESTful API 核心概念

在第一章中我们提到了 RESTful API，现在深入了解一下。

**REST (Representational State Transfer)** 是一种软件架构风格，它定义了一组约束，用于创建可伸缩的 Web 服务。符合 REST 风格的 API 被称为 RESTful API。

核心思想围绕着**资源 (Resources)**：
*   **资源**：API 中的一切都被视为资源。例如，我们的任务管理系统中的 `Task` 就是一个资源。资源通过唯一的 **URI (Uniform Resource Identifier)** 来标识。
*   **URI**：例如 `/tasks` 表示任务集合，`/tasks/1` 表示 ID 为 1 的任务。
*   **HTTP 方法 (HTTP Methods)**：对资源的操作通过 HTTP 方法来表示：
    *   `GET`：从服务器获取资源。安全 (safe)，幂等 (idempotent)。
    *   `POST`：向服务器提交新数据，通常用于创建新资源。不安全，不幂等。
    *   `PUT`：更新服务器上的资源（通常是完整替换）。不安全，幂等。
    *   `PATCH`：对服务器上的资源进行部分更新。不安全，不幂等。
    *   `DELETE`：从服务器删除资源。不安全，幂等。
*   **无状态 (Stateless)**：每个请求都包含处理该请求所需的所有信息，服务器不保存客户端的上下文信息。这意味着每个请求都是独立的。
*   **表现层 (Representational)**：客户端和服务器通过表示形式 (如 JSON, XML) 来交换资源的状态。对于 Web API，JSON 是最常见的选择。

## 2. Flask 基础

### 什么是 Flask？

Flask 是一个用 Python 编写的轻量级 Web 服务器网关接口 (WSGI) Web 应用框架。它被称为“微框架”，因为它核心功能精简，易于扩展，不强制使用特定的数据库、ORM 或其他库。这给了开发者极大的自由度，但也意味着你需要自己选择和集成其他组件。

### 安装 Flask

确保你已经激活了项目的虚拟环境 (参阅 02_环境搭建与版本控制.md)。

```bash
# 如果还没有安装，这会安装 Flask
pip install Flask
# 确认安装成功
pip show Flask
```

我们的 `requirements.txt` 中已经包含了 Flask，所以 `pip install -r requirements.txt` 会自动安装。

### `app.py`：应用入口

让我们回顾一下 `code/task_app/app.py`。这是 Flask 应用的入口点。

```python
# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy() # 初始化 SQLAlchemy 实例，但尚未绑定到 Flask 应用

def create_app():
    app = Flask(__name__) # 创建 Flask 应用实例
    app.config.from_object(Config) # 从 Config 对象加载配置

    db.init_app(app) # 将 SQLAlchemy 实例与 Flask 应用绑定

    # 导入并注册蓝图 (Blueprints)
    # 蓝图用于组织和管理路由，让大型应用更模块化
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks') # 注册蓝图，并设置 URL 前缀

    # 在应用上下文外创建数据库表
    # 只有在应用启动时，需要确保数据库表存在。在生产环境中，这通常通过数据库迁移工具完成。
    with app.app_context():
        db.create_all()

    @app.route('/') # 定义一个根路由
    def index():
        return jsonify({"message": "Welcome to the Task Management API!"}) # 返回 JSON 响应

    return app

if __name__ == '__main__':
    app = create_app() # 创建应用
    app.run(debug=True) # 运行应用，debug=True 开启调试模式 (开发环境使用)
```

**核心点：**
*   `Flask(__name__)`：创建 Flask 应用实例。
*   `app.config.from_object(Config)`：加载我们在 `config.py` 中定义的配置。
*   `db.init_app(app)`：将 `SQLAlchemy` 实例 `db` 绑定到 `app`。我们会在 `models.py` 中使用这个 `db` 实例来定义模型。
*   **蓝图 (Blueprint)**：`tasks_bp = Blueprint('tasks', __name__)`。蓝图是 Flask 提供的一种组织应用的方式，可以将相关的路由、视图函数和模板组织在一起，使其模块化。这对于构建大型应用尤其有用。
*   `app.register_blueprint(tasks_bp, url_prefix='/tasks')`：注册蓝图，并指定 URL 前缀为 `/tasks`。这意味着 `tasks_bp` 中定义的所有路由都会以 `/tasks` 为前缀。
*   `@app.route('/')`：这是一个装饰器，用于将 URL `/` 绑定到 `index` 函数，当用户访问 `/` 时，就会执行 `index` 函数并返回其结果。
*   `jsonify(...)`：Flask 提供的一个辅助函数，用于将 Python 字典或列表转换为 JSON 格式的 HTTP 响应。
*   `app.run(debug=True)`：启动开发服务器。`debug=True` 会在代码修改时自动重启服务器，并提供详细的错误信息，非常适合开发阶段。

### `config.py`：配置管理

`code/task_app/config.py` 文件用于存放应用程序的配置。

```python
# config.py
import os

class Config:
    # 数据库连接 URI，优先从环境变量 DATABASE_URL 获取，否则使用 SQLite 文件
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/tasks.db'
    # 关闭 Flask-SQLAlchemy 事件追踪功能，节省资源
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask 应用的密钥，用于会话管理等，生产环境应使用强随机密钥并从环境变量获取
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
```

**核心点：**
*   `SQLALCHEMY_DATABASE_URI`：指定数据库连接字符串。`sqlite:///instance/tasks.db` 表示在项目根目录下的 `instance` 文件夹中创建一个名为 `tasks.db` 的 SQLite 数据库文件。
*   `SECRET_KEY`：Flask 应用的安全密钥，用于加密会话 cookie 等。**在生产环境中，务必使用一个复杂的、随机生成的密钥，并通过环境变量进行设置，不要硬编码在此处。**

## 3. `routes.py`：API 路由定义与实现

`code/task_app/routes.py` 是我们定义所有 API 路由的地方。它使用 Flask 蓝图来组织这些路由。

```python
# routes.py
from flask import Blueprint, request, jsonify
from .models import Task # 从 models.py 导入 Task 模型
from .app import db     # 从 app.py 导入 db 实例

tasks_bp = Blueprint('tasks', __name__) # 创建一个名为 'tasks' 的蓝图

# --- 获取所有任务 (GET /tasks) ---
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all() # 查询所有任务
    return jsonify([task.to_dict() for task in tasks]) # 将任务对象列表转换为 JSON 返回

# --- 获取单个任务 (GET /tasks/<task_id>) ---
@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # 根据 ID 获取任务，如果不存在则返回 404 错误
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()) # 返回单个任务的 JSON 数据

# --- 创建任务 (POST /tasks) ---
@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json() # 获取请求体中的 JSON 数据
    if not data or not 'title' in data: # 验证数据是否包含 title 字段
        return jsonify({"error": "Title is required"}), 400 # 400 Bad Request

    # 创建新的 Task 对象
    new_task = Task(
        title=data['title'],
        description=data.get('description'), # .get() 方法可以提供默认值，避免 KeyError
        status=data.get('status', 'pending'),
        due_date=data.get('due_date')
    )
    db.session.add(new_task) # 将新任务添加到数据库会话
    db.session.commit()      # 提交会话，保存到数据库
    return jsonify(new_task.to_dict()), 201 # 返回新创建的任务和 201 Created 状态码

# --- 更新任务 (PUT /tasks/<task_id>) ---
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id) # 获取任务
    data = request.get_json() # 获取请求体中的 JSON 数据

    # 更新任务属性，如果请求体中没有提供则保持不变
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.due_date = data.get('due_date', task.due_date)

    db.session.commit() # 提交会话
    return jsonify(task.to_dict()) # 返回更新后的任务数据

# --- 删除任务 (DELETE /tasks/<task_id>) ---
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id) # 获取任务
    db.session.delete(task) # 从数据库会话中删除任务
    db.session.commit() # 提交会话
    return '', 204 # 返回空响应和 204 No Content 状态码
```

**核心点：**
*   `Blueprint('tasks', __name__)`：创建一个蓝图实例。
*   `@tasks_bp.route(...)`：使用蓝图实例的 `route` 装饰器来定义路由，而不是 `app.route`。
*   `methods=['GET', 'POST', ...]`：指定该路由允许的 HTTP 方法。
*   `request.get_json()`：获取客户端发送的 JSON 格式请求体数据。
*   `jsonify(...)`：将 Python 对象转换为 JSON 响应。
*   `Task.query.all()`, `Task.query.get_or_404(task_id)`：这些是 SQLAlchemy 提供的查询方法，用于从数据库中获取数据。`get_or_404` 如果找不到资源会自动返回 404 错误。
*   `db.session.add(obj)`, `db.session.commit()`, `db.session.delete(obj)`：这些是 SQLAlchemy 提供的数据库会话操作，用于添加、保存和删除数据库中的数据。
*   **HTTP 状态码**：每个响应都应该返回合适的 HTTP 状态码，例如 `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`。

## 4. `models.py`：数据库模型定义

`code/task_app/models.py` 定义了 `Task` 数据库模型，它映射到数据库中的 `task` 表。

```python
# models.py
from datetime import datetime
from .app import db # 从 app 模块导入 db 实例 (这是 Flask-SQLAlchemy 的约定)

class Task(db.Model):
    # 定义表名，默认是类名的小写形式 (task)
    # __tablename__ = 'tasks'

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
            'created_at': self.created_at.isoformat() if self.created_at else None, # 转换为 ISO 格式字符串
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
```

**核心点：**
*   `Task(db.Model)`：`Task` 类继承自 `db.Model`，告诉 Flask-SQLAlchemy 这是一个数据库模型。
*   `db.Column(...)`：定义了表的每一列。参数包括：
    *   `db.Integer`, `db.String(length)`, `db.DateTime`：数据类型。
    *   `primary_key=True`：设为主键。
    *   `nullable=False`：不允许为空。
    *   `default=...`：设置默认值。
    *   `onupdate=datetime.utcnow`：每次更新记录时，自动更新此字段的值。
*   `to_dict()` 方法：这是一个非常实用的方法，用于将 `Task` 对象的属性封装成一个字典。在 API 响应中，我们通常需要返回 JSON 格式的数据，`jsonify()` 可以直接处理字典列表，所以这个方法很有用。

## 5. 运行你的第一个 Flask API

现在，我们已经有了完整的 Flask 应用、数据库模型和 API 路由。让我们来运行它！

1.  **确保在 `code/task_app` 目录下**：
    ```bash
    cd Knowledge/python-production-tutorial/code/task_app
    ```
2.  **激活虚拟环境**：
    ```bash
    source venv/bin/activate # macOS/Linux
    # venv\Scripts\activate # Windows
    ```
3.  **安装依赖 (如果尚未安装)**：
    ```bash
    pip install -r requirements.txt
    ```
4.  **运行应用**：
    ```bash
    python app.py
    ```
    你会看到类似以下的输出：
    ```
     * Debug mode: on
     * Running on http://127.0.0.1:5000
     * Press CTRL+C to quit
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: XXX-XXX-XXX
    ```

现在，你的 API 已经在 `http://127.0.0.1:5000` 上运行了！你可以使用工具 (如 Postman, Insomnia, curl) 或在浏览器中测试。

### 测试 API (使用 `curl` 命令)

1.  **访问根目录 (GET /)**：
    ```bash
    curl http://127.0.0.1:5000/
    ```
    预期响应：`{"message":"Welcome to the Task Management API!"}`

2.  **创建任务 (POST /tasks)**：
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"title": "学习 Python", "description": "完成 Python 生产实践教程", "due_date": "2024-12-31"}' http://127.0.0.1:5000/tasks
    ```
    预期响应：返回新创建的任务对象，包含 `id` 和其他字段。

3.  **获取所有任务 (GET /tasks)**：
    ```bash
    curl http://127.0.0.1:5000/tasks
    ```
    预期响应：一个包含所有任务的 JSON 数组。

4.  **获取单个任务 (GET /tasks/1)** (假设 ID 为 1 的任务已创建)：
    ```bash
    curl http://127.0.0.1:5000/tasks/1
    ```
    预期响应：ID 为 1 的任务详情。

5.  **更新任务 (PUT /tasks/1)**：
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"status": "in_progress"}' http://127.0.0.1:5000/tasks/1
    ```
    预期响应：更新后的任务对象，`status` 字段变为 `in_progress`。

6.  **删除任务 (DELETE /tasks/1)**：
    ```bash
    curl -X DELETE http://127.0.0.1:5000/tasks/1
    ```
    预期响应：空响应，HTTP 状态码 204 No Content。

恭喜你！你已经成功构建并运行了你的第一个具备完整 CRUD 功能的 RESTful API。下一章我们将学习如何为这个 API 编写自动化测试，确保它的健壮性和正确性。
