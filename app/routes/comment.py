from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Comment, Course, User, db
#  评论蓝图，前缀为/comments, 下面路由传入的地址前面都必须带上前缀
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
        return jsonify({'message': 'Course not found'}), 404

    new_comment = Comment(user_id=current_user['id'], course_id=course_id, content=content, star=star)# 创建一条评论
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment created successfully'}), 201

@comment_bp.route('/<int:comment_id>', methods=['PUT'])# put方法用于更新评论
@jwt_required()
def update_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment or comment.user_id != current_user['id']:# 只能更新自己的评论
        return jsonify({'message': 'Comment not found or unauthorized'}), 404

    data = request.get_json()
    comment.content = data.get('content', comment.content)
    db.session.commit()

    return jsonify({'message': 'Comment updated successfully'}), 200

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])# 删除评论
@jwt_required()
def delete_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment or comment.user_id != current_user['id']:
        return jsonify({'message': 'Comment not found or unauthorized'}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'}), 200

@comment_bp.route('/<int:course_id>', methods=['GET'])# 获取某个课程的所有评论
def get_comments_by_course(course_id):
    comments = Comment.query.filter_by(course_id=course_id).all()
    return jsonify([{'id': c.id, 'user_id': c.user_id, 'content': c.content, 'likes': c.likes} for c in comments])


@comment_bp.route('/<int:comment_id>', methods=['POST'])# 点赞评论
@jwt_required()
def like_comment(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    if current_user['id'] in comment.liked_by:
        # 如果已经点赞过了, 再点一次就取消点赞
        comment.likes -= 1
        comment.liked_by.remove(current_user['id'])
        db.session.commit()
        return jsonify({'message': 'Comment unliked successfully'}), 200
    else:
        comment.likes += 1
        comment.liked_by.append(current_user['id'])
        db.session.commit()
        return jsonify({'message': 'Comment liked successfully'}), 200
    