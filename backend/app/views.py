from flask import Blueprint, request, flash, jsonify
from sqlalchemy import text
import json

from . import db
from model.semantic_comparison import get_embedding

views_bp = Blueprint('views', __name__)

@views_bp.route('/search/<string:tagname>', methods=['POST'])
def search_relevant_news(tagname: str):
    top_n_rank = request.args.get('top_n_rank', default=20, type=int)
    if len(tagname) < 1:
        flash('tagname is too short!', category='error') 
        return {'error': 'tagname is too short'}, 400

    vector = json.dumps(get_embedding(tagname).tolist())
    result = db.session.execute(
        text(f"""SELECT news_id, title, cat_lv1, cat_lv2, keywords, url, date
            FROM news_embedding ORDER BY embedding <=> '{vector}' LIMIT {top_n_rank}""")
    )

    news = [{
        "news_id": row[0], 
        "title": row[1], 
        "cat_lv1": row[2], 
        "cat_lv2": row[3], 
        "keywords": row[4], 
        "url": row[5], 
        "date": row[6]} 
    for row in result]

    return {'news': news}
