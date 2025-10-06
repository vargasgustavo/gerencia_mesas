import jwt
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from .config import Config


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(hash_pw: str, password: str) -> bool:
    return check_password_hash(hash_pw, password)


def generate_token(payload: dict) -> str:
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'message': 'Authorization header missing'}), 401

        parts = auth.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'message': 'Invalid authorization header'}), 401

        token = parts[1]
        try:
            data = decode_token(token)
            request.user = data
        except Exception as e:
            return jsonify({'message': 'Invalid or expired token', 'error': str(e)}), 401

        return f(*args, **kwargs)

    return decorated
