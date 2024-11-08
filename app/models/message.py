from datetime import datetime

from app import db 

class Message(db.Model):
    __tablename__ = 'Message'
    '''用户与消息的关系'''
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), primary_key=True)
    message = db.Column(db.String(1000))
    read = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.now, primary_key=True)
