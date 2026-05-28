# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 导入并注册蓝图
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # 在应用上下文外创建数据库表
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Task Management API!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
