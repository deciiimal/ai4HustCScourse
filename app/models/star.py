from app import db 

class Star(db.Model):
    '''用户与课程的收藏关系'''
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey('Course.courseid'), primary_key=True)