from http import HTTPStatus
from re import search
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Course, make_success_response, make_error_response, History


search_bp = Blueprint('search', __name__)


@search_bp.route('/course', methods=['GET'])
def search_by_coursename():
    pattern = request.args.get('kw').strip()
    if not pattern:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'search keyword can not be empty'
        )
    
    search_pattern = f'%{pattern}%'
    
    courses = Course.query.filter(Course.coursename.like(search_pattern)).all()
    
    courses_list = [
        {
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image-url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        } for course in courses
    ]
    
    return make_success_response(
        course=courses_list
    )
    

@search_bp.route('/teacher', methods=['GET'])
def search_by_teacher():
    pattern = request.args.get('kw').strip()
    if not pattern:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'search keyword can not be empty'
        )
    
    courses = Course.query.filter(Course.teachername==pattern).all()
    
    courses_list = [
        {
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image-url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        } for course in courses
    ]
    
    return make_success_response(
        course=courses_list
    )
    
@search_bp.route('/', methods=['GET'])
@jwt_required()
def search_by_all():
    pattern = request.args.get('kw').strip()
    if not pattern:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'search keyword can not be empty'
        )
    search_pattern = f'%{pattern}%'
    
    courses1 = Course.query.filter(Course.coursename.like(search_pattern)).all()
    courses2 = Course.query.filter(Course.teachername==pattern).all()
    
    courses_list1 = [
        {
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image-url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        } for course in courses1
    ]
    courses_list2 = [
        {
            'courseid': course.courseid, 
            'name': course.coursename, 
            'description': course.description,
            'likes-count': course.likes_count,
            'comments-count': course.comments_count,
            'image-url': course.image_url,
            'teacher': course.teachername,
            'category': course.category
        } for course in courses2
    ]
        # Check if the search keyword already exists in the history
    userid = get_jwt_identity()
    existing_history = History.query.filter_by(userid=userid, kw=pattern).first()
    if not existing_history:
        # If not, add it to the history
        new_history = History(userid = userid, kw=pattern)
        db.session.add(new_history)
        db.session.commit()
    return make_success_response(
        # Check if the user is authenticated
        course=courses_list1 + courses_list2
    )
    
@search_bp.route('/history', methods=['GET'])
@jwt_required()
def get_search_history():
    userid = get_jwt_identity()
    histories = History.query.filter_by(userid=userid).all()
    history_list = [
        history.kw for history in histories
    ]
    if len(history_list) > 10:
        history_list = history_list[:10]
    return make_success_response(
        history=history_list
    )