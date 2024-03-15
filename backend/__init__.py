from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

from .config import POSTGRES_URI

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config["SECRET_KEY"] = str(uuid.uuid4())
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
    db.init_app(app)

    from .models import NewsEmbedding

    with app.app_context():
        db.create_all()

    # register blueprints
    from .api.routes import api_bp
    from .views import views_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)

    return app
