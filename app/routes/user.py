from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
# 用户蓝图
user_bp = Blueprint('user', __name__)

# 用户注册
@user_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role', 'user')  # 默认是普通用户
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # 创建新用户
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'})

# 用户登录
@user_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=username).first()# 调用User的query方法，filter_by为条件筛选
    # 查询返回的是一个list，调用.first得到第一个对象
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 登录用户
    login_user(user)
    return jsonify({'message': 'User logged in successfully', 'role': user.role})


