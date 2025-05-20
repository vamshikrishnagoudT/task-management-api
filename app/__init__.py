from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

task_dependencies = db.Table(
    'task_dependencies',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('depends_on_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes.user import user_bp
    from app.routes.project import project_bp
    from app.routes.task import task_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')

    with app.app_context():
        db.create_all()

    return app