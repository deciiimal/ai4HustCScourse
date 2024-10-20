import flask 

def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    
    from .routes import user
    app.register_blueprint(user.bp)
    
    with app.app_context():
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
    
    return app