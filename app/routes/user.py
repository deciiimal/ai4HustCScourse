import flask 
from flask import Blueprint, request

import json

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route('/login', methods=['POST'])
def login():
    info = request.json
    print(info)
    
    return "login OK"
    
@bp.route('/register', methods=['POST'])
def register():
    info = request.json
    print(info)
    
    return "register OK"
       
    
