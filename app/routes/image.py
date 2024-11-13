from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, make_error_response, make_success_response
from app.utils import admin_required
from app.utils import decode_image, encode_image
from app.utils import format_avatar, check_avatar, save_avatar, load_avatar, generate_avator_name
from app.utils import format_cover, check_cover, save_cover, load_cover, generate_cover_name

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
    
    image = decode_image(
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
    
    if not check_avatar(avatar):
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
        
    base64_image = encode_image(image)
    
    return make_success_response(
        image=base64_image
    )
    

@image_bp.route('/avatar/d/<int:userid>', methods=['GET'])
def get_avatar_by_userid(userid: int):
    avatar = generate_avator_name(userid)
    
    if not check_avatar(avatar):
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            f'no user {userid} or user do not have a avatar'
        )
        
    image = load_avatar(avatar)
    
    if image is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'not found'
        )
        
    base64_image = encode_image(image)
    
    return make_success_response(
        image=base64_image
    )
    
##################################################

@image_bp.route("/cover", methods=['POST'])
@admin_required
def upload_cover():
    
    data = request.get_json()
    
    if 'image' not in data.keys() or 'courseid' not in data.keys():
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'a image file required'
        )
        
    base64_image: str = data.get('image')
    courseid = int(data.get('courseid'))
    
    image = decode_image(
        base64_image=base64_image
        )
    
    if image is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'base64 bytes is illegal'
        )
        
    image = format_cover(image)
    
    filename = generate_cover_name(
        courseid=courseid
    )
    
    save_cover(
        image=image,
        filename=filename
    )
    
    return make_success_response()


@image_bp.route('/cover/filename/<int:courseid>', methods=['GET'])
def get_cover_name(courseid):
    cover = generate_cover_name(courseid)
    if not check_cover(cover):
        cover = ''
    
    return make_success_response(
        cover=cover
    )
    
    
@image_bp.route('/cover/<string:filename>', methods=['GET'])
def get_cover(filename: str):
    image = load_cover(filename)
    
    if image is None:
        return make_error_response(
            HTTPStatus.BAD_REQUEST,
            'not found'
        )
        
    base64_image = encode_image(image)
    
    return make_success_response(
        image=base64_image
    )