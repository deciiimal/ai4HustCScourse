from http import HTTPStatus

from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app import db
from app.models import User, make_error_response, make_success_response

# 用户蓝图
user_bp = Blueprint('user', __name__)

# 用户注册
@user_bp.route('/register', methods=['POST'])
def register():
    info = request.get_json()

    username = info.get('username')
    password = info.get('password')
    email = info.get('email')
    
    if not username or not password or not email:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username, password and email are required'
        )
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username already exists'
        )
        
    # 创建新用户
    hashed_password = generate_password_hash(password)
    user: User = User(username=username, password=hashed_password, email=email)
    
    db.session.add(user)
    db.session.commit()
    
    token = create_access_token(
        identity=user.userid,
        additional_claims={
            'role': user.role
        }
    )
    
    return make_success_response(
        userid=user.userid,
        username=user.username,
        role=user.role,
        token=token
    )

# 用户登录
@user_bp.route('/login', methods=['POST'])
def login():
    info = request.get_json()
    
    username = info.get('username')
    password = info.get('password')
    if not username or not password:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username and password are required'
        )
    
    # 查找用户
    user: User = User.query.filter_by(username=username).first()# 调用User的query方法，filter_by为条件筛选
    # 查询返回的是一个list，调用.first得到第一个对象
    if not user or not check_password_hash(user.password, password):
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            'Invalid username or password'
        )
        
    if user.banned:
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            f'Current user {user.username} is banned'
        )
        
    token = create_access_token(# 把jwt生成并返回给前端
        identity=user.userid,
        additional_claims={
            'role': user.role
        }
    )
    
    # 登录用户
    return make_success_response(
        userid=user.userid,
        username=user.username,
        role=user.role,
        userInfo=token# jwt
    )


