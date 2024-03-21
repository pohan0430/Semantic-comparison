from flask import Blueprint, request, flash, jsonify
from sqlalchemy import text
import json
import sys
from typing import List
sys.path.append('../')

from . import db
from model.semantic_comparison import get_embedding

views_bp = Blueprint('views', __name__)

@views_bp.route('/search/<string:tagname>', methods=['POST'])
def search_relevant_news(tagname: str):
    top_n_rank = request.args.get('top_n_rank', default=20, type=int)
    if len(tagname) < 1:
        flash('tagname is too short!', category='error') 
        return jsonify({'error': 'tagname is too short'}), 400

    vector = json.dumps(get_embedding(tagname).tolist())
    result = db.session.execute(
        text(f"""SELECT title, cat_lv1, cat_lv2, keywords, url, date
            FROM news_embedding ORDER BY embedding <=> '{vector}' LIMIT {top_n_rank}""")
    )

    news = [{
        "title": row[0], 
        "cat_lv1": row[1], 
        "cat_lv2": row[2], 
        "keywords": row[3], 
        "url": row[4], 
        "date": row[5]} 
    for row in result]

    return jsonify({'news': news})
