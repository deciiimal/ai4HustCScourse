from datetime import datetime

from app import db


class Comment(db.Model):
    '''评论属性有：评论id，用户id，课程id，评论内容，点赞数'''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    stars = db.Column(db.Integer, default=0)# 评论的星级
    likes = db.Column(db.Integer, default=0)# 每一个评论都有点赞数
    time = db.Column(db.DateTime, default=datetime.now)# 评论时间
    liked_by = []# 评论被谁点赞了
