from . import db
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import validates, backref
from .config import EMBEDDING_LENGTH

class NewsEmbedding(db.Model):
    news_id = db.Column(db.Text, primary_key=True)
    embedding = db.Column(Vector(EMBEDDING_LENGTH))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    children_new_id = db.relationship(
        "NewsTag",
        cascade="all, delete",
    )

class Users(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String(64))

class Tag(db.Model):
    tag = db.Column(db.Text, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    username = db.Column(db.String, db.ForeignKey('users.username'), default='admin')
    children_tag = db.relationship(
        "NewsTag",
        cascade="all, delete",
    )

class NewsTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.Text, db.ForeignKey('news_embedding.news_id', ondelete='CASCADE'))
    tag = db.Column(db.Text, db.ForeignKey('tag.tag', ondelete='CASCADE'))

@validates('username')
def validate_username(self, key, value):
    if not (4 <= len(value) <= 30):
        raise ValueError("Text length must be between 4 and 30 characters.")
    return value

@validates('password')
def validate_password(self, key, value):
    if not (8 <= len(value) <= 20):
        raise ValueError("Text length must be between 4 and 20 characters.")
    return value
