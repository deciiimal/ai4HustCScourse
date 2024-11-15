from datetime import datetime

from app import db 

class CourseStar(db.Model):
    __tablename__ = 'CourseStar'
    '''用户与课程的收藏关系'''
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey('Course.courseid'), primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now, primary_key=True)

class CommentStar(db.Model):
    __tablename__ = 'CommentStar'
    '''用户与评论的点赞关系'''
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), primary_key=True)
    commentid = db.Column(db.Integer, db.ForeignKey('Comment.commentid'), primary_key=True)
    