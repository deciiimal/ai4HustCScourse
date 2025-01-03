import os
import flask
import json
import sched
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI

db = SQLAlchemy()
jwt = JWTManager()
scheduler: sched.scheduler = None
kiwi_client: OpenAI = None
running_config = {}

def create_app():
    app = flask.Flask(__name__)
    
    config_path = os.path.join(app.root_path, 'config', 'config.json')
    
    if os.path.exists(config_path):
        app.config.from_file("./config/config.json", load=json.load)
        print(f"load config.json at {config_path}")
    else:
        app.config.from_file("./config/config.example.json", load=json.load)
        print(f"no config.json found, use example")
        
    
    db.init_app(app)
    jwt.init_app(app)
    
    global kiwi_client
    kiwi_client = OpenAI(
        api_key=app.config.get("KIWI_API_KEY"),
        base_url=app.config.get("KIWI_BASE_URL")
    )
    
    global running_config
    running_config = {
        k: v for (k, v) in app.config.items()
    }
    
    global scheduler
    # scheduler = sched.scheduler(
        
    # )
    
    print('running configuration:')
    for (k, v) in running_config.items():
        print(f'\t{k}: {v}')
    else:
        print()
    
    # 注册蓝图
    from .routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')# url_prefix表示公共前缀
    
    from .routes import course_bp
    app.register_blueprint(course_bp, url_prefix='/course')
    
    from .routes import comment_bp
    app.register_blueprint(comment_bp, url_prefix='/comment')

    from .routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from .routes import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    from .routes import search_bp
    app.register_blueprint(search_bp, url_prefix='/search')
    
    from .routes import image_bp
    app.register_blueprint(image_bp, url_prefix='')

    for rule in app.url_map.iter_rules():
        print(f'path: {rule.rule}\tmethod: {rule.methods}')

    return app
    