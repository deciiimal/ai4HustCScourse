from http import HTTPStatus

from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, make_error_response, make_success_response, Message
from app.utils import generate_avator_name, check_avatar

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
        token=token# jwt
    )

# 查看消息中心
@user_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    user_id = get_jwt_identity()
    
    messages = Message.query.filter_by(userid=user_id).all()
    if not messages:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'No messages found for this user'
        )
    
    messages_data = [
        {
            'message': msg.message,
            'create_time': msg.time,
            'been_read': msg.read
        }
        for msg in messages
    ]
    for msg in messages:
        msg.read = True
    db.session.commit()
    return make_success_response(messages=messages_data)

# 修改用户名
@user_bp.route('/username', methods=['PUT'])
@jwt_required()
def update_username():
    user_id = get_jwt_identity()
    new_username = request.get_json().get('username')
    if not new_username:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username is required'
        )
    
    if User.query.filter_by(username=new_username).first():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'the Username has been taken'
        )
    
    user = User.query.get(user_id)
    if not user:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'User not found'
        )
    
    user.username = new_username
    db.session.commit()
    
    return make_success_response(
        message='Username updated successfully'
    )

# 修改邮箱
@user_bp.route('/email', methods=['PUT'])
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    new_email = request.get_json().get('email')
    if not new_email:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'email is required'
        )
    
    if User.query.filter_by(email=new_email).first():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            '邮箱已被绑定'
        )
    
    user = User.query.get(user_id)
    if not user:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'User not found'
        )
    
    user.email = new_email
    db.session.commit()
    
    return make_success_response(
        message='email updated successfully'
    )

# 修改密码
@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    if not old_password or not new_password or not confirm_password:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Old password, new password, and confirmation are required'
        )
    
    if new_password != confirm_password:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'New password and confirmation do not match'
        )
    
    user = User.query.get(user_id)
    if not user or not check_password_hash(user.password, old_password):
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            'Invalid old password'
        )
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return make_success_response(
        message='Password updated successfully'
    )
    

# 获取个人信息
@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_myinfo():
    userid = get_jwt_identity()
    
    user: User = User.query.get(userid)
    
    avatar = generate_avator_name(user.userid)
    if not check_avatar(avatar):
        avatar = ''
    
    return make_success_response(
        userid=user.userid,
        username=user.username,
        avatar=avatar,
        email=user.email,
        banned=user.banned,
        create_at=user.create_time
    )
    

# 获取其他人信息
@user_bp.route('/<int:userid>', methods=['GET'])
@jwt_required()
def get_info(userid):
    
    user: User | None = User.query.get(userid)
    
    if user is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            f'no user {userid}'
        )
        
    avatar = generate_avator_name(user.userid)
    if not check_avatar(avatar):
        avatar = ''
        
    return make_success_response(
        userid=user.userid,
        username=user.username,
        avatar=avatar,
        email=user.email,
        banned=user.banned,
        create_at=user.create_time
    )