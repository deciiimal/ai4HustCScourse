from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, make_error_response, make_success_response, user
from app.utils import decode_avatar, format_avatar, save_avatar, generate_avator_name


image_bp = Blueprint('image', __name__)


@image_bp.route("/avatar", methods=['POST'])
@jwt_required()
def upload_avatar():
    userid = get_jwt_identity()
    
    data = request.get_json()
    
    if 'image' not in data.keys() or 'extension' not in data.keys():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'a png/jpg file required'
        )
        
    base64_image: str = data.get('image')
    extension: str = data.get('extension')
    
    image = decode_avatar(
        base64_image=base64_image
        )
    
    if image is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'base64 bytes is illegal'
        )
        
    image = format_avatar(image)
    
    filename = generate_avator_name(
        userid=userid,
        extension=extension
    )
    
    save_avatar(
        image=image,
        filename=filename
    )
    
    return make_success_response()