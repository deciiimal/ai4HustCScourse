from functools import wraps
from http import HTTPStatus
from typing import Callable, Tuple

from flask_jwt_extended import get_jwt, jwt_required
from flask import Response, jsonify

from app.models import Role, make_error_response

def admin_required(fn: Callable[[], Tuple[Response, HTTPStatus]]):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt()
        if user.get('role') != Role.Admin.value:
            return make_error_response(
                HTTPStatus.FORBIDDEN,
                'admin is required to do this'
            )
            
        return fn(*args, **kwargs)
    return wrapper
