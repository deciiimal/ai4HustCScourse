from http import HTTPStatus
from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Message, Comment, Course, User, make_error_response, make_success_response, CommentStar
from app.routes.image import get_avatar_by_userid
import json

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            f'no comment {comment_id}'
        )
    avatar = get_avatar_by_userid(comment.userid)
    if avatar[1] == HTTPStatus.OK: 
        avatar_data = json.loads(avatar[0].data)
        avatar = 'data:image/webp;base64,' + avatar_data['data']['image']
    else: avatar = "../../images/user1.png"
    return make_success_response(
        comment={
            "commentid": comment.commentid,
            "userid": comment.userid,
            "username": User.query.get(comment.userid).username,
            "avatar": avatar,
            "courseid": comment.courseid,
            "parent_commentid": comment.parent_commentid,
            "likes_count": comment.likes_count,
            "content": comment.content,
            "timestamp": comment.create_time,
            "star": comment.star
        }
    )

@comment_bp.route('/', methods=['POST'])# POST方法用于创建评论
@jwt_required()# 特定身份的用户才能访问，jwt表示json web token
def create_comment():# 创建一条评论
    current_userid = get_jwt_identity()# 返回用户id
    data = request.get_json()
    course_id = data.get('courseid')# 请求的json数据中必须要有course_id和content字段
    existing_comment = Comment.query.filter_by(userid=current_userid, courseid=course_id, parent_commentid=None).first()
    if existing_comment:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'You have already commented on this course'
        )
    
    content = data.get('content')# 获取评论内容
    star = data.get('star')# 获取评论星级

    current_user = User.query.filter_by(userid = current_userid).first()# 获取当前用户
    if current_user.banned:# 如果用户被封禁
        return make_error_response(
            HTTPStatus.FORBIDDEN,
            'You are banned by administator, please contact admin for more information'
        )
    
    if not Course.query.get(course_id):# get方法还真能用，可能就是匹配第一个是不是course_id
        return make_error_response(
            HTTPStatus.NOT_FOUND, 
            'Course not found'
        )

    if star not in [1,2,3,4,5]:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'Star must be an integer between 1 and 5'
        )
    
    new_comment = Comment(userid=current_userid, courseid=course_id, content=content, star=star)# 创建一条评论
    db.session.add(new_comment)
    db.session.commit()

    return make_success_response(
        message='Comment created successfully'
    )

@comment_bp.route('/<int:comment_id>', methods=['PUT'])# put方法用于更新评论
@jwt_required()
def update_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.filter_by(commentid = comment_id).first()

    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )
        
    if comment.userid != current_user:# 只能更新自己的评论
        return make_error_response(
            HTTPStatus.UNAUTHORIZED,
            'You can\'t update other user\'s comment'
        )

    data = request.get_json()
    comment.content = data.get('content')
    comment.star = data.get('star')
    comment.create_time = datetime.now
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
    if comment.userid != current_user:
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

    star = CommentStar.query.filter_by(userid=current_user, commentid=comment_id).first()
    
    if request.method == 'POST' and star is None:
        star = CommentStar(userid=current_user, commentid=comment_id)
        comment.likes_count += 1
        
        db.session.add(star)
        db.session.commit()
        
        course = Course.query.filter_by(courseid=comment.courseid).first()
        if not course:
            return make_error_response(
                HTTPStatus.NOT_FOUND,
                'Course not found'
            )
        current_user = User.query.filter_by(userid=current_user).first()
        message = f'你在《{course.coursename}》课程中的评论被用户 {current_user.username} 点赞了'
        new_message = Message(userid=comment.userid, message=message)
        db.session.add(new_message)
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

# 获取自己的所有评论
@comment_bp.route('/my_comments', methods=['GET'])
@jwt_required()
def get_my_comments():
    current_user = get_jwt_identity()
    comments = Comment.query.filter_by(userid=current_user).all()
    
    comments_data = [
        {
            'commentid': comment.commentid,
            'courseid': comment.courseid,
            'coursename': Course.query.get(comment.courseid).coursename,
            'content': comment.content,
            'star': comment.star,
            'created_at': comment.create_time
        }
        for comment in comments
    ]
    
    return make_success_response(
        comments=comments_data# 得知道这个参数然后读取？
    )
    
# 获得所有我点赞的评论
@comment_bp.route('/my_likes', methods=['GET'])
@jwt_required()
def get_my_likes():
    current_user = get_jwt_identity()
    stars = CommentStar.query.filter_by(userid=current_user).all()
    
    comments_data = [
        {
            'commentid': star.commentid,
            'courseid': Comment.query.get(star.commentid).courseid,
            'userid': Comment.query.get(star.commentid).userid,
            'username': User.query.get(Comment.query.get(star.commentid).userid).username,
            'content': Comment.query.get(star.commentid).content,
            'star': Comment.query.get(star.commentid).star,
            'create_at': Comment.query.get(star.commentid).create_time
        }
        for star in stars
    ]
    
    return make_success_response(
        comments=comments_data
    )
    
# 创建子评论
@comment_bp.route('/<int:comment_id>/reply', methods=['POST'])
@jwt_required()
def reply_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )
    existing_comment = Comment.query.filter_by(userid=current_user, courseid=comment.courseid, parent_commentid=comment_id).first()
    if existing_comment:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'You have already commented on this comment'
        )
    data = request.get_json()
    content = data.get('content')
    
    new_comment = Comment(userid=current_user, courseid=comment.courseid, parent_commentid=comment_id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    
    course = Course.query.filter_by(courseid=comment.courseid).first()
    if not course:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Course not found'
        )
    current_user = User.query.filter_by(userid=current_user).first()
    message = f'你在《{course.coursename}》课程中的评论被用户 {current_user.username} 评论了'
    new_message = Message(userid=comment.userid, message=message)
    db.session.add(new_message)
    db.session.commit()
    
    return make_success_response(
        message='Reply created successfully'
    )
    
@comment_bp.route('/<int:comment_id>/replies', methods=['GET'])
def get_replies(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return make_error_response(
            HTTPStatus.NOT_FOUND,
            'Comment not found'
        )
    
    replies = Comment.query.filter_by(parent_commentid=comment_id).all()
    
    replies_data = [
        {
            'commentid': reply.commentid,
            'courseid': reply.courseid,
            'userid': reply.userid,
            'content': reply.content,
            'star': reply.star,
            'created_at': reply.create_time
        }
        for reply in replies
    ]
    
    return make_success_response(
        replies=replies_data
    )