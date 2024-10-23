from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.user import user_bp
from routes.course import course_bp
from routes.comment import comment_bp
from routes.admin import admin_bp
# from routes.analysis import analysis_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/user')# url_prefix表示公共前缀
app.register_blueprint(course_bp, url_prefix='/courses')
app.register_blueprint(comment_bp, url_prefix='/comments')
app.register_blueprint(admin_bp, url_prefix='/admin')
# app.register_blueprint(analysis_bp, url_prefix='/analysis')

if __name__ == '__main__':
    app.run(debug=True)
