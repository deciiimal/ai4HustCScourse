import flask
import json

from flask_jwt_extended import JWTManager
from .models import db


def create_app():
    app = flask.Flask(__name__)
    
    app.config.from_file("./config/config.json", load=json.load)
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    # 注册蓝图
    from .routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')# url_prefix表示公共前缀
    
    from .routes import course_bp
    app.register_blueprint(course_bp, url_prefix='/courses')
    
    from .routes import comment_bp
    app.register_blueprint(comment_bp, url_prefix='/comments')

    from .routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # from routes import analysis_bp
    # app.register_blueprint(analysis_bp, url_prefix='/analysis')

    return app
    