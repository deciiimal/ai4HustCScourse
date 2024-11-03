from datetime import datetime
import enum

from app import db


class ClassCategory(enum.Enum):
    CORE_COURSE = "专业核心课"
    ELECTIVE_COURSE = "专业选修课"
    
class Course(db.Model):
    __tablename__ = 'Course'
    '''课程属性有: courseid, coursename, description, like数, comment数, 创建时间'''
    courseid = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(100), nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    image_url = db.Column(db.String(255), nullable=True)
    teachername = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(10), nullable=False)
    
    