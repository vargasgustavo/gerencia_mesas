from flask import Blueprint, request, jsonify, current_app
from ..models.auth import AuthModel
from ..utils import generate_token, verify_password
from ..database import get_db


bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/login', methods=['POST'])
def login():
data = request.json or {}
username = data.get('username')
password = data.get('password')
if not username or not password:
return jsonify({'message': 'username and password required'}), 400
user = AuthModel.find_by_username(username)
if not user:
return jsonify({'message': 'Invalid credentials'}), 401
# user['password_hash'] exists
if not verify_password(user['password_hash'], password):
return jsonify({'message': 'Invalid credentials'}), 401
payload = {'user_id': user['id'], 'username': user['username']}
token = generate_token(payload)
# persist token if desired
return jsonify({'message': 'Login realizado com sucesso', 'token': token, 'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}})


@bp.route('/register', methods=['POST'])
def register():
data = request.json or {}
username = data.get('username')
email = data.get('email')
password = data.get('password')
if not username or not email or not password:
return jsonify({'message': 'username, email and password required'}), 400
try:
user_id = AuthModel.create_user(username, email, password)
return jsonify({'message': 'User created', 'id': user_id}), 201
except Exception as e:
return jsonify({'message': 'Error creating user', 'error': str(e)}), 500


@bp.route('/verify', methods=['GET'])
def verify():
from ..utils import token_required
@token_required
def inner():
return jsonify({'message': 'Token válido', 'user': request.user}), 200
return inner()


@bp.route('/logout', methods=['POST'])
def logout():
# Optionally persist token revocation in DB
return jsonify({'message': 'Logout realizado'}), 200