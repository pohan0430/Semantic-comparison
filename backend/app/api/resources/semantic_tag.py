from flask_restful import Resource
from flask import jsonify, Response, request
from sqlalchemy.exc import SQLAlchemyError

from app.models import Tag, NewsEmbedding, NewsTag, Users
from app import db


class SemanticTag(Resource):
    def get(self, tagname: str):
        exist = db.session.query(Tag.query.filter_by(tag=tagname).exists()).scalar()
        if not exist:
            return {"error": f"Tag {tagname} not found"}, 404

        result = (
            db.session.query(NewsEmbedding).join(NewsTag).filter_by(tag=tagname).all()
        )
        news = [
            {
                "title": row.title,
                "cat_lv1": row.cat_lv1,
                "cat_lv2": row.cat_lv2,
                "keywords": row.keywords,
                "url": row.url,
                "date": row.date,
            }
            for row in result
        ]

        return jsonify({"news": news})

    def post(self, tagname: str):
        try:
            relevant_news_id = request.json.get("news_id", None)
            if not relevant_news_id or len(relevant_news_id) == 0:
                return {"error": "No news_id provided for tagging"}, 400

            db.session.add(Tag(tag=tagname))

            for news_id in relevant_news_id:
                db.session.add(NewsTag(news_id=news_id, tag=tagname))
            db.session.commit()

            response = jsonify({"tagname": tagname})
            response.status_code = 201
            response.headers["Location"] = f"tag/{tagname}"
            return response
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Failed to create {tagname} tag, error:{e}"}, 500

    def delete(self, tagname: str):
        tag = Tag.query.filter_by(tag=tagname).first()

        if tag:
            try:
                db.session.delete(tag)
                db.session.commit()
                return Response(status=204)
            except SQLAlchemyError as e:
                db.session.rollback()
                return {"error": f"Failed to delete {tagname} tag"}, 500

        return {"error": f"Tag {tagname} not found."}, 404

    def put(self, tagname):
        return {"data": f"put {tagname}!"}


class SemanticTagList(Resource):
    def get(self):
        result = Tag.query.with_entities(Tag.tag).all()
        tags = [row[0] for row in result]
        return {"tags": tags}
