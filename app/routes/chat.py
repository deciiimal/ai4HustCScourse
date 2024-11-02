from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import ChatHistory, MessageRole, Comment, Course, make_error_response, make_success_response
from utils import kiwi, kiwi_format_history, kiwi_create_prompt

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/<int:courseid>", methods=["GET", "POST", "DELETE"])
@jwt_required()
def chat(courseid):
    userid = get_jwt_identity()

    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
    
    if request.method == "DELETE": 
        
        ChatHistory.query.filter_by(userid=userid, courseid=courseid).delete()
        db.session.commit()
        
        return make_success_response()
    
    chat_history = (ChatHistory.query
                    .with_entities(ChatHistory.message_role, ChatHistory.content, ChatHistory.timestamp)
                    .filter_by(userid=userid, courseid=courseid)
                    .order_by(ChatHistory.timestamp)
                    .all()
                    )
    
    if request.method == "GET":
        return make_success_response(
            messages=[{
                    "index": index,
                    "role": item.message_role,
                    "content": item.content,
                    "timestamp": item.timestamp
                } for index, item in enumerate(chat_history) 
                if item.message_role in (MessageRole.USER.value, MessageRole.ASSISTANT.value)
            ]
        )
    
    if len(chat_history) == 0:
        course = (Course.query
                  .with_entities(Course.coursename, Course.description)
                  .get(courseid)
                  )
        comments = (Comment.query
                    .with_entities(Comment.content)
                    .filter_by(userid=userid, courseid=courseid)
                    .all()
                    )
        context = kiwi_create_prompt(message, course, comments)
    else:
        context = kiwi_format_history(chat_history)
    
    response = kiwi(message, context)
    
    new_chat = ChatHistory(
        userid=userid,
        courseid=courseid,
        message_role=response['role'],
        content=response['content']
    )
    
    db.session.add(new_chat)
    db.session.commit()
    
    return make_success_response(
        messages=[{
            "index": 0,
            "role": new_chat.message_role,
            "content": new_chat.content,
            "timestamp": new_chat.timestamp
        }]
    )
