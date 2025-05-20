from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from app.models.user import User
from app import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated