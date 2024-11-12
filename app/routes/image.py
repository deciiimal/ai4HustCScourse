from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, make_error_response, make_success_response
from app.utils import decode_avatar, encode_avatar, format_avatar, check_avatar_file, save_avatar, load_avatar, generate_avator_name


image_bp = Blueprint('image', __name__)


@image_bp.route("/avatar", methods=['POST'])
@jwt_required()
def upload_avatar():
    userid = get_jwt_identity()
    
    data = request.get_json()
    
    if 'image' not in data.keys():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'a image file required'
        )
        
    base64_image: str = data.get('image')
    
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
        userid=userid
    )
    
    save_avatar(
        image=image,
        filename=filename
    )
    
    return make_success_response()


@image_bp.route('/avatar/filename/<int:userid>', methods=['GET'])
def get_avatar_name(userid):
    avatar = generate_avator_name(userid)
    if not check_avatar_file(avatar):
        avatar = ''
    
    return make_success_response(
        avatar=avatar
    )
    

@image_bp.route('/avatar/<string:filename>', methods=['GET'])
def get_avatar(filename: str):
    image = load_avatar(filename)
    
    if image is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'not found'
        )
        
    base64_image = encode_avatar(image)
    
    return make_success_response(
        image=base64_image
    )