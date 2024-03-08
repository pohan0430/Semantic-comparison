from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy import text
import random
import json

from . import db

views_bp = Blueprint('views', __name__)

@views_bp.route('/search', methods=['POST'])
def search_relevant_news():
    # keyword = request.form.get('keyword') # Gets the keyword from the HTML 
    keyword = '便宜美食的文章'

    if len(keyword) < 1:
        flash('keyword is too short!', category='error') 
    else:
        # get embedding
        vector = json.dumps([random.uniform(-1, 1) for _ in range(128)])
        result = db.session.query(
            text(f"select news_id FROM news_embedding ORDER BY embedding <-> '{vector}' LIMIT 20")
        )

    return jsonify([row for row in result])
