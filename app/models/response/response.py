from http import HTTPStatus
from flask import jsonify

def make_success_response(http_status=HTTPStatus.OK, message='', **kwargs):
    return jsonify({
        'status': 'success',
        'data': kwargs,
        'message': message
    }), http_status
    
def make_error_response(http_status: HTTPStatus, error=''):
    return jsonify({
        'status': 'error',
        'error': error,
    }), http_status