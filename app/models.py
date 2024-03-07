from . import db
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import mapped_column

class NewsEmbedding(db.Model):
    news_id = db.Column(db.Text, primary_key=True)
    embedding = db.Column(Vector(128))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
