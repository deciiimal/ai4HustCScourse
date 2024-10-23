from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 初始化数据库对象db，并创建多个模型类

db = SQLAlchemy()

class User(db.Model):# 就是一个数据库，里面存放了相同类型的元数据
    '''用户属性有：id，用户名，密码，角色类型'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user') # 'user' or 'admin'
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
class Course(db.Model):
    '''课程属性有：id，课程名，课程描述'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    likes = db.Column(db.Integer, default=0)# 每一个课程都有点赞数
    liked_by = []# 课程被谁点赞了
    

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
