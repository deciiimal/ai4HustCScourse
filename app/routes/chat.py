from http import HTTPStatus
from re import U

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import ChatHistory, MessageRole, Comment, Course, make_error_response, make_success_response
from app.utils import kiwi, kiwi_format_history, kiwi_create_prompt

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/<int:courseid>", methods=["POST"])
@jwt_required()
def chat(courseid):
    print("chat")
    userid = get_jwt_identity()

    data = request.get_json()
    message = data.get("message")
    
    new_history = []
    
    chat_history = (ChatHistory.query
                    .with_entities(ChatHistory.message_role, ChatHistory.content, ChatHistory.timestamp)
                    .filter_by(userid=userid, courseid=courseid)
                    .order_by(ChatHistory.timestamp)
                    .all()
                    )
    
    if len(chat_history) == 0:
        course = (Course.query
                  .get(courseid)
                  )
        comments = (Comment.query
                    .with_entities(Comment.content, Comment.star)
                    .filter_by(courseid=courseid)
                    .all()
                    )
        context = kiwi_create_prompt(message, course, comments)
    
        for c in context:
            new_history.append(ChatHistory(
                userid=userid,
                courseid=courseid,
                message_role=c['role'],
                content=c['content']
            ))
    else:
        context = kiwi_format_history(chat_history)
        
    # print('message: ', message)
    # print('context: ', '\n'.join(str(item) for item in context))
    
    response, status = kiwi(message, context)
    
    if status is False:
        return make_error_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            'sorry, we can not handle this so far'
        )
    
    new_history.append(ChatHistory(
        userid=userid,
        courseid=courseid,
        message_role=MessageRole.USER.value,
        content=message
    ))
    
    new_history.append(ChatHistory(
        userid=userid,
        courseid=courseid,
        message_role=response['role'],
        content=response['content']
    ))
    
    for item in new_history:
        db.session.add(item)
    db.session.commit()
    
    return make_success_response(
        messages=[{
            "index": 0,
            "role": new_history[-1].message_role,
            "content": new_history[-1].content,
            "timestamp": new_history[-1].timestamp
        }]
    )


@chat_bp.route("/<int:courseid>", methods=["GET"])
@jwt_required()
def get_chat(courseid):
    userid = get_jwt_identity()

    chat_history = (ChatHistory.query
                    .with_entities(ChatHistory.message_role, ChatHistory.content, ChatHistory.timestamp)
                    .filter_by(userid=userid, courseid=courseid)
                    .order_by(ChatHistory.timestamp)
                    .all()
                    )
    
    return make_success_response(
        messages=[{
                "index": index,
                "role": item.message_role,
                "content": item.content,
                "timestamp": item.timestamp
            } for index, item in enumerate(item
                for item in chat_history 
                if item.message_role in (MessageRole.USER.value, MessageRole.ASSISTANT.value)
            ) 
        ]
    )


@chat_bp.route("/<int:courseid>", methods=["DELETE"])
@jwt_required()
def delete_chat(courseid):
    userid = get_jwt_identity()
    
    ChatHistory.query.filter_by(userid=userid, courseid=courseid).delete()
    db.session.commit()
    
    return make_success_response()