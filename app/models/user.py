from app import db

class User(db.Model):# 就是一个数据库，里面存放了相同类型的元数据
    '''User : userid，username, password, email, role, banned'''
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, default=0) # 'user' or 'admin'
    banned = db.Column(db.Boolean, default=False)
