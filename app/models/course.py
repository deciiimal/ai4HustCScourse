from datetime import datetime

from app import db

    
class Course(db.Model):
    '''课程属性有: courseid，coursename，description, like数, comment数'''
    courseid = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(100), nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    