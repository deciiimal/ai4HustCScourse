from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, Role, Course, Comment, make_error_response, make_success_response
from app.utils import admin_required

# 管理员蓝图
admin_bp = Blueprint('admin', __name__)

# 管理员注册
@admin_bp.route('/register', methods=['POST'])
def register():
    info = request.get_json()

    username = info.get('username')
    password = info.get('password')
    email = info.get('email')
    invite_code = info.get('invite_code')
    
    if not username or not password or not email or not invite_code:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username, password, email and invite_code are required'
        )
    
    if invite_code != "114514":
        '''邀请码之后还需要搞一个数据库存储'''
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'invite_code is not exist or invalid'
        )
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Username already exists'
        )
        
    # 创建新用户
    hashed_password = generate_password_hash(password)
    user: User = User(username=username, password=hashed_password, email=email, role=Role.Admin.value)
    
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

# 管理员登录
@admin_bp.route('/login', methods=['POST'])
def login():
    info = request.get_json()
    
    username = info.get('username')
    password = info.get('password')
    if not username or not password:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'username and password are required'
        )
    
    # 查找用户
    user: User = User.query.filter_by(username=username).first()# 调用User的query方法，filter_by为条件筛选

    if not user or not check_password_hash(user.password, password):
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            'Invalid username or password'
        )
        
    token = create_access_token(
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
        userInfo=token
    )

#################################对用户的操作######################################

@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])# 对用户禁言
@admin_required# 对jwt进一步解析，需要是管理员才行
def ban_user(user_id):
    user = User.query.filter_by(userid=user_id).first()
    if not user:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'User not found'
        )

    user.banned = True
    db.session.commit()

    return make_success_response(
        message = 'User banned successfully'
    )

@admin_bp.route('/users/<int:user_id>/unban', methods=['POST'])# 对用户解禁言
@admin_required# 对jwt进一步解析，需要是管理员才行
def unban_user(user_id):
    user = User.query.filter_by(userid=user_id).first()
    if not user:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'User not found'
        )

    user.banned = False
    db.session.commit()

    return make_success_response(
        message = 'User unbanned successfully'
    )

#################################对课程的操作######################################
@admin_bp.route('/courses', methods=['POST'])# 加入课程
@admin_required
def create_course():
    data = request.get_json()
    # courseid 自动加，就不用处理了
    new_course = Course(coursename=data['name'], description=data['description'])
    db.session.add(new_course)
    db.session.commit()
    return make_success_response(
        message=f"Course {data['name']} created successfully"
    )

@admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])# 删除课程
@admin_required
def delete_course(course_id):
    course = Course.query.filter_by(courseid=course_id).first()
    if not course:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Course not found'
        )

    db.session.delete(course)
    db.session.commit()

    return make_success_response(
        message=f'Course {course.coursename} deleted successfully'
    )
#################################对评论的操作######################################

@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(commentid=comment_id).first()
    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )

    db.session.delete(comment)
    db.session.commit()

    return make_success_response(
        message='Comment deleted successfully'
    )
