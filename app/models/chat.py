from datetime import datetime
import enum

from app import db

class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatHistory(db.Model):
    __tablename__ = 'ChatHistory'
    
    chatid = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 重命名对话 ID
    userid = db.Column(db.Integer, db.ForeignKey('User.userid'), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey('Course.courseid'), nullable=False)
    message_role = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)