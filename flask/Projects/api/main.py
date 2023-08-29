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


## 회원가입
## http -v POST http://localhost:5000/sign-up name=seungbeen email=tmdqls6625@naver.com password=1234
@app.route("/sign-up", methods=["POST"])
def sign_up():
    new_user = request.json
    # db_conn.execute(text("SELECT * FROM users"))
    new_user_id = app.database.execute(
        text(
            """
    INSERT INTO users_profile (
        name,
        email,
        profile,
        hashed_password
    ) VALUES (
        :name,
        :email,
        :profile,
        :password
        )

                                                 """
        ),
        new_user,
    ).lastrowid

    row = current_app.database.execute(
        text(
            """
        SELECT
        id,
        name,
        email,
        profile
        FROM users_profile
        WHERE id = :user_id                 
                                            """
        ),
        {"user_id": new_user_id},
    ).fetchone()

    id_, name, email, profile = row
    create_user = (
        {
            "id": id_,
            "name": name,
            "email": email,
            "profile": profile,
        }
        if row
        else None
    )
    app.database.commit()
    return jsonify(create_user)


## 트윗
## http -v POST http://localhost:5000/tweets id:=1 tweet="My first tweet"
@app.route("/tweet", methods=["POST"])
def tweet():
    payloads = request.json
    tweet_data = payloads["tweet"]
    tweet_name = payloads["name"]

    user_id_row = current_app.database.execute(
        text("SELECT id FROM users_profile WHERE name = :name"),
        {"name": tweet_name},
    ).fetchone()
    app.database.commit()
    if not user_id_row:
        return "사용자가 존재하지 않습니다.", 400

    user_id = user_id_row[0]  # Extract the user ID from the row

    # Insert the tweet into the tweets table
    tweet_insert = current_app.database.execute(
        text(
            """
            INSERT INTO tweets (
                user_id,
                tweet
            ) VALUES (
                :user_id,
                :tweet
            )
            """
        ),
        {"user_id": user_id, "tweet": tweet_data},
    )
    app.database.commit()
    # Get the last inserted row's ID
    last_inserted_id = tweet_insert.lastrowid

    # Fetch the inserted tweet from the database
    row = current_app.database.execute(
        text(
            """
            SELECT
                id,
                user_id,
                tweet
            FROM tweets
            WHERE id = :tweet_id
            """
        ),
        {"tweet_id": last_inserted_id},
    ).fetchone()

    if not row:
        return "문제가 발생하였습니다.", 500

    id_, user_id, tweet = row
    create_tweet = {"id": id_, "user_id": user_id, "tweet": tweet}

    return jsonify(create_tweet), 200


## 사용자 팔로우하기
@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])

    if user_id not in app.users and user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    user = app.users[user_id]
    user.setdefault("follow", set()).add(user_id_to_follow)

    return jsonify(user)


## 사용자 언팔로우하기


@app.route("/unfollow", methods=["POST"])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["unfollow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    user = app.users[user_id]
    user.setdefault("follow", set()).discard(user_id_to_follow)

    return jsonify(user)


## 사용자 타임라인 만들기
@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    follow_list = app.users[user_id].get("follow", set)
    follow_list.add(user_id)

    timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]

    return jsonify({"user_id": user_id, "timeline": timeline})
