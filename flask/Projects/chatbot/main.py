from flask import Flask, jsonify, request, render_template, current_app
from flask.json import JSONEncoder
import db_config
from sqlalchemy import create_engine, text

import mysql.connector


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_pyfile("db_config.py")
    else:
        app.config.update(test_config)
    db = create_engine(app.config["DB_URL"], max_overflow=0)
    db_conn = db.connect()

    app.database = db_conn
    app.database_conn = db_conn
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


## flask 에서 set을 json으로 바꾸는 클래스
class CustomerJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


app.json_encoder = CustomerJSONEncoder
app.id_count = 1
app.users = {}
app.tweets = []


## 핑체크
@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


## 카테고리 추가
## http -v POST http://localhost:5000/sign-up name=seungbeen email=tmdqls6625@naver.com password=1234
@app.route("/category", methods=["POST"])
def category():
    new_category = request.json

    type_id = app.database.execute(
        text(
            """
    INSERT INTO info_category (
        type
    ) VALUES (
        :type
        )

                                                 """
        ),
        new_category,
    ).lastrowid

    row = current_app.database.execute(
        text(
            """
        SELECT
        id,
        type
        FROM info_category
        WHERE id = :type_id
                                            """
        ),
        {"type_id": type_id},
    ).fetchone()

    id_, type = row
    create_type = (
        {
            "id": id_,
            "type": type,
        }
        if row
        else None
    )
    app.database.commit()
    return jsonify(create_type)


# ## 트윗
# ## http -v POST http://localhost:5000/tweets id:=1 tweet="My first tweet"
# @app.route("/tweet", methods=["POST"])
# def tweet():
#     payloads = request.json
#     tweet_data = payloads["tweet"]
#     tweet_name = payloads["name"]

#     user_id_row = current_app.database.execute(
#         text("SELECT id FROM users_profile WHERE name = :name"),
#         {"name": tweet_name},
#     ).fetchone()
#     app.database.commit()
#     if not user_id_row:
#         return "사용자가 존재하지 않습니다.", 400

#     user_id = user_id_row[0]  # Extract the user ID from the row

#     # Insert the tweet into the tweets table
#     tweet_insert = current_app.database.execute(
#         text(
#             """
#             INSERT INTO tweets (
#                 user_id,
#                 tweet
#             ) VALUES (
#                 :user_id,
#                 :tweet
#             )
#             """
#         ),
#         {"user_id": user_id, "tweet": tweet_data},
#     )
#     app.database.commit()
#     # Get the last inserted row's ID
#     last_inserted_id = tweet_insert.lastrowid

#     # Fetch the inserted tweet from the database
#     row = current_app.database.execute(
#         text(
#             """
#             SELECT
#                 id,
#                 user_id,
#                 tweet
#             FROM tweets
#             WHERE id = :tweet_id
#             """
#         ),
#         {"tweet_id": last_inserted_id},
#     ).fetchone()

#     if not row:
#         return "문제가 발생하였습니다.", 500

#     id_, user_id, tweet = row
#     create_tweet = {"id": id_, "user_id": user_id, "tweet": tweet}

#     return jsonify(create_tweet), 200
