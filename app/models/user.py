from app import db
import re
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, self.email))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        return jwt.encode(
            {
                'user_id': self.id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
            },
            Config.SECRET_KEY,
            algorithm='HS256'
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }