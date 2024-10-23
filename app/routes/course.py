from flask import Blueprint, request, jsonify
from app.models import Course, db, Comment
from flask import abort
from flask_login import current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
# 课程蓝图
course_bp = Blueprint('course', __name__)# 创建一个蓝图，蓝图的前缀在app.py中指定

@course_bp.route('/', methods=['GET'])# 使用GET方法直接访问该蓝图（/course），返回所有课程
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in courses])

# 点赞课程
@jwt_required()
def like_course(course_id):
    current_user_id = get_jwt_identity()
    course = Course.query.get(course_id)

    if not course:
        return jsonify({'message': 'Course not found'}), 404

    if current_user_id in course.liked_by:
        # 如果已经点赞过了, 再点一次就取消点赞
        course.likes -= 1
        course.liked_by.remove(current_user_id)
        db.session.commit()
        return jsonify({'message': 'Course unliked successfully'}), 200
    else:
        course.likes += 1
        course.liked_by.append(current_user_id)
        db.session.commit()
        return jsonify({'message': 'Course liked successfully'}), 200
    
# 查看某门课程的全部评论
@course_bp.route('/<int:course_id>/comments', methods=['GET'])
def get_course_comments(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({'message': 'Course not found'}), 404

    comments = Comment.query.filter_by(course_id=course_id).all()
    comments_list = [{'id': comment.id, 'user_id': comment.user_id, 'content': comment.content, 'timestamp': comment.timestamp} for comment in comments]
    return jsonify(comments_list), 200
