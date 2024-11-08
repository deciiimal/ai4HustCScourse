from datetime import datetime

from app import db 

class History(db.Model):
    __tablename__ = 'History'
    '''用户与消息的关系'''
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), primary_key=True)
    kw = db.Column(db.String(100), primary_key=True)
