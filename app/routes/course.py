from http import HTTPStatus
from flask import Blueprint, request, jsonify, abort
from flask_login import current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Star, Course, Comment, make_success_response, make_error_response, user

# 课程蓝图
course_bp = Blueprint('course', __name__)# 创建一个蓝图，蓝图的前缀在app.py中指定

@course_bp.route('/', methods=['GET'])# 使用GET方法直接访问该蓝图（/course），返回所有课程
def get_courses():
    courses = Course.query.all()
    return make_success_response(
        courses=courses
    )

# 获取自己的点赞情况，点赞，取消点赞
@course_bp.route('/<int:courseid>/like', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def like_course(courseid):
    userid = get_jwt_identity()
    
    course = Course.query.get(courseid)
    if course is None:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            f'no course {courseid}'
        )

    star = Star.query.filter_by(userid=userid, courseid=courseid).first()
    
    if request.method == 'POST' and star is None:
        star = Star(userid=userid, courseid=courseid)
        course.likes_count += 1
        
        db.session.add(star)
        db.session.commit()
    
    elif request.method == 'DELETE' and star is not None:
        course.likes_count -= 1
        
        db.session.delete(star)
        db.session.commit()
    
    elif request.method == 'GET':
        return make_success_response(
            liked=star is not None
        )
        
    return make_success_response()
    
# 查看某门课程的全部评论
@course_bp.route('/<int:courseid>/comments', methods=['GET'])
def get_course_comments(courseid):
    course = Course.query.get(courseid)

    if not course:
        return jsonify({'message': 'Course not found'}), 404

    comments = Comment.query.filter_by(course_id=courseid).all()
    comments_list = [{'id': comment.id, 'user_id': comment.user_id, 'content': comment.content, 'timestamp': comment.timestamp} for comment in comments]
    return jsonify(comments_list), 200
