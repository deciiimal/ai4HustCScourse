from datetime import datetime
import enum



from app import db

class Role(enum.Enum):
    User = 0
    Admin = 1

class User(db.Model):# 就是一个数据库，里面存放了相同类型的元数据
    __tablename__ = 'User'
    '''User : userid，username, password, email, role, banned'''
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, default=Role.User.value) # 'user' or 'admin'
    banned = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

