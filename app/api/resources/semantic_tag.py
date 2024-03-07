from flask_restful import Resource

class SemanticTag(Resource):
    def get(self, tagname):
        return {'data': f'get {tagname}!'}
    def post(self, tagname):
        return {'data': f'post {tagname}!'}
    def delete(self, tagname):
        return {'data': f'delete {tagname}!'}
    def put(self, tagname):
        return {'data': f'put {tagname}!'}

class SemanticTagList(Resource):
    def get(self):
        return {'data': 'get tag list'}
