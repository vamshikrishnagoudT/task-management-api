from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    with app.app_context():
        db.create_all()

    return app