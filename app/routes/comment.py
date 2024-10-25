from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
#  评论蓝图，前缀为/comments, 下面路由传入的地址前面都必须带上前缀
from http import HTTPStatus
from app import db
from app.models import Comment, Course, User, make_error_response, make_success_response, CommentStar

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])# POST方法用于创建评论
@jwt_required()# 特定身份的用户才能访问，jwt表示json web token
def create_comment():# 创建一条评论
    current_user = get_jwt_identity()# 获取当前用户的身份信息，返回一个字典，包含用户的id和email
    data = request.get_json()
    course_id = data.get('course_id')# 请求的json数据中必须要有course_id和content字段
    content = data.get('content')# 获取评论内容
    star = data.get('star')# 获取评论星级

    if not Course.query.get(course_id):# 如果没有这个课程
        return make_error_response(
            HTTPStatus.NOT_FOUND, 
            'Course not found'
        )

    new_comment = Comment(user_id=current_user['id'], course_id=course_id, content=content, star=star)# 创建一条评论
    db.session.add(new_comment)
    db.session.commit()

    return make_success_response(
        message='Comment created successfully'
    )

@comment_bp.route('/<int:comment_id>', methods=['PUT'])# put方法用于更新评论
@jwt_required()
def update_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )
        
    if comment.user_id != current_user['id']:# 只能更新自己的评论
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            'You can\'t update other user\'s comment'
        )

    data = request.get_json()
    comment.content = data.get('content', comment.content)
    db.session.commit()

    return make_success_response(
        message='Comment updated successfully'
    )

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])# 删除评论
@jwt_required()
def delete_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )
    if comment.user_id != current_user['id']:
        return make_success_response(
            HTTPStatus.UNAUTHORIZED,
            'You can\'t delete other user\'s comment'
        )

    db.session.delete(comment)
    db.session.commit()

    return make_success_response(
        message='Comment deleted successfully'
    )

# 获取自己的点赞情况，点赞，取消点赞
@comment_bp.route('/<int:comment_id>/like', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def like_comment(comment_id):
    current_user = get_jwt_identity()
    
    comment = Comment.query.get(comment_id)
    if comment is None:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            f'Comment {comment_id} not found'
        )

    star = CommentStar.query.filter_by(user_id=current_user['id'], comment_id=comment_id).first()
    
    if request.method == 'POST' and star is None:
        star = CommentStar(user_id=current_user['id'], comment_id=comment_id)
        comment.likes_count += 1
        
        db.session.add(star)
        db.session.commit()
    
    elif request.method == 'DELETE' and star is not None:
        comment.likes_count -= 1
        
        db.session.delete(star)
        db.session.commit()
    
    elif request.method == 'GET':
        return make_success_response(
            liked=star is not None
        )
        
    return make_success_response()
