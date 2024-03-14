from flask_restful import Resource
from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError

from backend.models import Tag, NewsEmbedding, NewsTag, Users
from backend.views import get_relevant_news_id
from backend import db

class SemanticTag(Resource):
    def get(self, tagname: str):
        exist = db.session.query(Tag.query.filter_by(tag=tagname).exists()).scalar()
        if not exist:
            response = jsonify({'error': f'Tag {tagname} not found'})
            response.status_code = 404
            return response

        result = NewsTag.query.filter_by(tag=tagname).with_entities(NewsTag.news_id).all()
        news_id = [row[0] for row in result]

        return jsonify({'news_id': news_id})


    def post(self, tagname: str):
        try:
            # add tag
            db.session.add(Tag(tag=tagname))
            db.session.commit()

            # add news_tag
            relevant_news_id = get_relevant_news_id(tagname)
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
