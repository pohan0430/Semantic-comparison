from flask_restful import Resource
from flask import jsonify, Response, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import json
from typing import List
import sys
sys.path.append('../')

from backend.models import Tag, NewsEmbedding, NewsTag, Users
from backend import db
from model.semantic_comparison import get_embedding

class SemanticTag(Resource):
    def get(self, tagname: str):
        exist = db.session.query(Tag.query.filter_by(tag=tagname).exists()).scalar()
        if not exist:
            response = jsonify({'error': f'Tag {tagname} not found'})
            response.status_code = 404
            return response

        result = db.session.query(NewsEmbedding).join(NewsTag).filter_by(tag=tagname).all()
        news = [{
            "title": row.title, 
            "cat_lv1": row.cat_lv1, 
            "cat_lv2": row.cat_lv2, 
            "keywords": row.keywords, 
            "url": row.url, 
            "date": row.date} 
        for row in result]

        return jsonify({'news': news})


    def post(self, tagname: str):
        try:
            data = request.json
            top_n_rank = data.get('top_n_rank', 20)
            # add tag
            db.session.add(Tag(tag=tagname))
            db.session.commit()

            vector = json.dumps(get_embedding(tagname).tolist())
            result = db.session.execute(
                text(f"SELECT news_id FROM news_embedding ORDER BY embedding <=> '{vector}' LIMIT {top_n_rank}")
            )

            relevant_news_id = [row[0] for row in result]

            for news_id in relevant_news_id:
                db.session.add(NewsTag(news_id=news_id, tag=tagname))
            db.session.commit()

            response = jsonify({'tagname': tagname})
            response.status_code = 201
            response.headers['Location'] = f'tag/{tagname}'
            return response
        except SQLAlchemyError as e:
            db.session.rollback()
            error_response = jsonify({'error': f'Failed to create {tagname} tag'})
            error_response.status_code = 500  # Internal Server Error
            return error_response


    def delete(self, tagname: str):
        tag = Tag.query.filter_by(tag=tagname).first()

        if tag:
            db.session.delete(tag)
            db.session.commit()
            return Response(status=204)

        return {'error': f'Tag {tagname} not found.'}, 404


    def put(self, tagname):
        return {'data': f'put {tagname}!'}


class SemanticTagList(Resource):
    def get(self):
        result = Tag.query.with_entities(Tag.tag).all()
        tags = [row[0] for row in result]
        return {'tags': tags}
