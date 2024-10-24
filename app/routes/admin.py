from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, Course, Comment
from app.utils import admin_required
# 管理员蓝图
admin_bp = Blueprint('admin', __name__)

# 管理员注册
@admin_bp.route('/register', methods=['POST'])
def admin_register():
    username = request.json.get('username')
    password = request.json.get('password')
    admin_invite_code = request.json.get('admin_invite_code')
    
    # 验证管理员邀请码
    if admin_invite_code != "114514":# 邀请码自己设
        return jsonify({'error': 'Invalid admin invite code'}), 403
    
    # 检查用户名和密码
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # 创建管理员用户
    hashed_password = generate_password_hash(password)
    new_admin = User(username=username, password=hashed_password, role='admin', is_admin=True)
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin registered successfully'})

# 管理员登录
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 查找用户并验证是否为管理员
    user = User.query.filter_by(username=username, role='admin').first()# user是从数据库中查找到的对象
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 登录管理员
    return jsonify({'message': 'Admin logged in successfully'})

#################################对用户的操作######################################

@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])# 对用户禁言
@jwt_required()# 对jwt字段进行解析，这个字段往往是后端生成发给前端由前端保存，然后对于需要进行身份验证的请求带上
@admin_required# 对jwt进一步解析，需要是管理员才行
def ban_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_banned = True
    db.session.commit()

    return jsonify({'message': 'User banned successfully'})


#################################对课程的操作######################################
@admin_bp.route('/courses', methods=['POST'])# 加入课程
@jwt_required()
@admin_required
def create_course():
    data = request.get_json()
    new_course = Course(name=data['name'], description=data['description'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully'})

@admin_bp.route('/courses/<int:course_id>', methods=['DELETE'])# 删除课程
@jwt_required()
@admin_required
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted successfully'})

#################################对评论的操作######################################

@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'})
