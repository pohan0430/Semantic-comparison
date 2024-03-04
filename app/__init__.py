from flask import Flask

def create_app():
    app = Flask(__name__)

    # register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app
