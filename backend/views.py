from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy import text
import random
import json
import sys
from typing import List
sys.path.append('../')

from . import db
from .config import EMBEDDING_LENGTH
from model.semantic_comparison import get_embedding

views_bp = Blueprint('views', __name__)

def get_relevant_news_id(tagname: str, top_n_rank: int=20) -> List[str]:
    vector = json.dumps(get_embedding(tagname).tolist())
    result = db.session.execute(
        text(f"SELECT news_id FROM news_embedding ORDER BY embedding <-> '{vector}' LIMIT {top_n_rank}")
    )

    relevant_news_id = [row[0] for row in result]
    return relevant_news_id

@views_bp.route('/search', methods=['POST'])
def search_relevant_news():
    data = request.json
    tagname = data.get('tagname', '')

    if len(tagname) < 1:
        flash('tagname is too short!', category='error') 
        return jsonify({'error': 'tagname is too short'}), 400

    relevant_news_id = get_relevant_news_id(tagname)

    return jsonify({'news_id': relevant_news_id})
