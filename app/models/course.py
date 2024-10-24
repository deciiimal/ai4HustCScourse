from app import db

    
class Course(db.Model):
    '''课程属性有: courseid，coursename，description, like数, comment数'''
    courseid = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    