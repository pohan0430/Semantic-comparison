import os
import sys
from flask import Flask, render_template, request, jsonify

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from model.semantic_comparison import find_similar_titles_urls


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    input_text = data.get("input_string", "")

    similar_titles_urls = find_similar_titles_urls(input_text)

    result = [
        {"title": title_url[0], "similarity": title_url[1]}
        for title_url in similar_titles_urls
    ]

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
