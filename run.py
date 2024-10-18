import flask 
from flask import request 
import json

app = flask.Flask(__name__)

@app.route('/user/login', methods=['POST'])
def login():
    info = request.json
    
    return json.dumps({"comment": "ok"})

@app.route('/')
def hello_world():
    return '<p>Hello World</p>'