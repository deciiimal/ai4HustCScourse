from http import HTTPStatus
from re import search
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Course, make_success_response, make_error_response


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
    