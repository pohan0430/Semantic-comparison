from flask import Blueprint
from flask_restful import Api
from backend.api.resources import SemanticTag, SemanticTagList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(SemanticTag, '/tag/<string:tagname>')
api.add_resource(SemanticTagList, '/tags')
