from flask import Blueprint, request, flash, jsonify
from sqlalchemy import text
import os
import json
import pandas
from pandas import DataFrame
import requests
import tempfile
from uuid import uuid4
from datetime import datetime

from . import db
from model.semantic_comparison import get_embedding

views_bp = Blueprint("views", __name__)


@views_bp.route("/search/<string:tagname>", methods=["POST"])
def search_relevant_news(tagname: str):
    top_n_rank = request.args.get("top_n_rank", default=20, type=int)
    if len(tagname) < 1:
        flash("tagname is too short!", category="error")
        return {"error": "tagname is too short"}, 400

    vector = json.dumps(get_embedding(tagname).tolist())
    result = db.session.execute(
        text(
            f"""SELECT news_id, title, cat_lv1, cat_lv2, keywords, url, date, img, audience
            FROM news_embedding ORDER BY embedding <=> '{vector}' LIMIT {top_n_rank}"""
        )
    )

    news = [
        {
            "news_id": row[0],
            "title": row[1],
            "cat_lv1": row[2],
            "cat_lv2": row[3],
            "keywords": row[4],
            "url": row[5],
            "date": row[6],
            "img": row[7],
            "audience": row[8],
        }
        for row in result
    ]
    print("here")
    result = db.session.execute(text("SELECT COUNT(*) FROM news_embedding"))
    count = result.scalar()
    print(f"count: {count}")
    print(f"news: {news}")

    return {"news": news}


@views_bp.route("/total_audience", methods=["POST"])
def total_audience():
    try:
        news_ids = request.json.get("news_ids", [])
        if not news_ids:
            return jsonify({"error": "No news IDs provided"}), 400

        print("Received news_ids:", news_ids)

        news_id_list = ",".join(map(str, news_ids))

        sql = f"""
        WITH user_view_news AS (
            SELECT et_token_hash AS et_token, news_id AS news_id
            FROM etl_custom_tag_autokeyword_audience_count_user_base
        ),
        filtered AS (
            SELECT et_token
            FROM user_view_news
            WHERE news_id IN ({news_id_list})
            GROUP BY et_token
        ),
        unique_audience AS (
            SELECT COUNT(DISTINCT et_token) AS unique_audience
            FROM filtered
        )
        SELECT unique_audience
        FROM unique_audience;
        """

        print("Generated SQL:", sql)

        play_session = (
            "a1fe64a720ceac9acb9729070b58c6f21ac78e5a-namespace=eds&username=app.dmp"
        )

        try:
            print("Sending request to dora.ettoday.net")
            resp = requests.post(
                "https://dora.ettoday.net/queryResult",
                headers={
                    "Cookie": f"PLAY_SESSION={play_session}",
                    "Content-Type": "application/x-www-form-urlencoded charset=UTF-8",
                },
                data={
                    "jobId": str(uuid4())[:8],
                    "limit": "unlimited",
                    "sql": sql,
                    "txDate": datetime.now().isoformat().replace("T", " ")[:19],
                },
                stream=True,
            )
            resp.raise_for_status()
            with tempfile.NamedTemporaryFile(suffix=".zip") as f:
                try:
                    dtype = None
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

                    df: DataFrame = pandas.read_csv(
                        f, sep="\t", compression="zip", encoding="utf-8", dtype=dtype
                    )
                except Exception as e:
                    print(resp.status_code)
                    print(resp.headers)
                    print(resp.content)
                    raise e
            df = df.convert_dtypes()
            print(df.columns)
            if "Exception" in df.columns[0]:
                print(df.iloc[0:1, 0].to_list())
                raise Exception(df.columns[0])

            df = df[[c for c in df.columns if not c.startswith("__")]]
            data = df.to_dict(orient="records")
            print("Response Data:", data)
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            print("Response status code:", resp.status_code if resp else "No response")
            print("Response text:", resp.text if resp else "No response text")
            return jsonify({"error": "Request failed"}), 500
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500
