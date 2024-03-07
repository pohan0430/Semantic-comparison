from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .configs import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
    db.init_app(app)

    from .models import NewsEmbedding

    with app.app_context():
        db.create_all()

    # register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app
