from http import HTTPStatus
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import CourseStar, Course, Comment, make_success_response, make_error_response, user
from app.utils import admin_required
from datetime import datetime, timedelta

# 课程蓝图
course_bp = Blueprint('course', __name__)# 创建一个蓝图，蓝图的前缀在app.py中指定

@course_bp.route('', methods=['GET'])# 使用GET方法直接访问该蓝图（/course），返回所有课程
def get_courses():
    courses = Course.query.all()
    course_list = [
        {
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image_url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        } for course in courses
    ]
    return make_success_response(
        course=course_list
    )
    
# 获取该课程详情
@course_bp.route('/<int:courseid>', methods=['GET'])
def get_one_course(courseid):
    course = Course.query.get(courseid)
    if course is None:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            f'no course {courseid}'
        )
    return make_success_response(
        course={
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image_url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        }
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

    star = CourseStar.query.filter_by(userid=userid, courseid=courseid).first()
    
    if request.method == 'POST' and star is None:
        star = CourseStar(userid=userid, courseid=courseid)
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
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Course not found'
        )

    comments = Comment.query.filter_by(courseid=courseid).all()
    comments_list = [
        {
            'commentid': comment.commentid,
            'courseid': comment.courseid,
            'userid': comment.userid,
            'content': comment.content,
            'star': comment.star,
            'create_at': comment.create_time
        } for comment in comments
    ]
    return make_success_response(
        comments=comments_list
    )

# 返回课程的所有数据，包括：总评论数、总收藏数、好评率、平均得分
@course_bp.route('/<int:courseid>/stats', methods=['GET'])
def get_course_stats(courseid):
    course = Course.query.get(courseid)
    
    if not course:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Course not found'
        )
    
    comments_count = Comment.query.filter_by(courseid=courseid).count()
    likes_count = course.likes_count
    positive_comments_count = Comment.query.filter(Comment.courseid == courseid, Comment.star > 3).count()
    average_score = db.session.query(db.func.avg(Comment.star)).filter_by(courseid=courseid).scalar()
     
    stats = {
        'comments_count': comments_count,
        'likes_count': likes_count,
        'positive_comments_count': positive_comments_count,
        'average_score': average_score
    }
    
    return make_success_response(
        stats=stats
    )


@course_bp.route('/<int:courseid>/draw', methods=['GET'])

def get_lastweek_comments_likes_trend(courseid):
    course = Course.query.get(courseid)
    
    if not course:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Course not found'
        )
    
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    
    comments_trend = [0] * 7
    likes_trend = [0] * 7
    
    comments = Comment.query.filter(Comment.courseid == courseid, Comment.create_time >= one_week_ago).all()
    likes = CourseStar.query.filter(CourseStar.courseid == courseid, CourseStar.create_time >= one_week_ago).all()
    
    for comment in comments:
        days_ago = (now - comment.create_time).days
        if days_ago < 7:
            comments_trend[6 - days_ago] += 1
    
    for like in likes:
        days_ago = (now - like.create_time).days
        if days_ago < 7:
            likes_trend[6 - days_ago] += 1
    
    return make_success_response(
        comments_trend=comments_trend,
        likes_trend=likes_trend
    )
