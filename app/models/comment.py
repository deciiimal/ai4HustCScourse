from datetime import datetime

from app import db


class Comment(db.Model):
    __tablename__ = "Comment"
    '''评论属性有: 评论id, 用户id, 课程id, 评论内容, 点赞数'''
    commentid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey('Course.courseid'), nullable=False)
    parent_commentid = db.Column(db.Integer, db.ForeignKey('Comment.commentid'), nullable=True)
    # 父评论id，表示该评论用于回复哪条评论
    likes_count = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)# 评论时间
    star = db.Column(db.Integer, default=0)# 1-5评分
    
