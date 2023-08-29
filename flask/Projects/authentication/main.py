from flask import Flask, jsonify, request, render_template, current_app
from flask.json import JSONEncoder
import db_config
from sqlalchemy import create_engine, text
import bcrypt
import jwt
from datetime import datetime, timedelta


def get_user(user_id):
    user = current_app.database.execute(
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
        {"user_id": user_id},
    ).fetchone()
    return (
        {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "profile": user["profile"],
        }
        if user
        else None
    )


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


@app.route("/login", methods=["POST"])
def login():
    credential = request.json
    email = credential["email"]
    password = credential["password"]

    row = current_app.database.execute(
        text(
            """
            SELECT
                id,
                hashed_password
            FROM users_profile
            WHERE email = :email
            """
        ),
        {"email": email},
    ).fetchone()
    id_, password_ = row
    if row and bcrypt.checkpw(password.encode("UTF-8"), password_.encode("UTF-8")):
        user_id = id_
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        print(app.config)
        token = jwt.encode(payload, "JWT_SECRET_KEY", "HS256")

        return jsonify({"access_token": token.decode("UTF-8")})
    else:
        return "", 401


## 회원가입
## http -v POST http://localhost:5000/sign-up name=seungbeen email=tmdqls6625@naver.com password=1234
@app.route("/sign-up", methods=["POST"])
def sign_up():
    new_user = request.json
    new_user["password"] = bcrypt.hashpw(
        new_user["password"].encode("UTF-8"), bcrypt.gensalt()
    )

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
    app.database.commit()
    new_user_info = get_user(new_user_id)
    return jsonify(new_user_info)


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
    user_name = int(payload["name"])
    user_id_row = current_app.database.execute(
        text("SELECT id FROM users_profile WHERE name = :name"),
        {"name": user_name},
    ).fetchone()
    app.database.commit()
    if not user_id_row:
        return "사용자가 존재하지 않습니다.", 400

    user_id = user_id_row[0]  # Extract the user ID from the row

    user_id_to_follow = int(payload["follow"])

    tweet_data = payloads["tweet"]
    tweet_name = payloads["name"]
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
    users_rows = current_app.database.execute(
        text(
            """
             SELECT 
             t.user_id,
             t.tweet 
             FROM tweets t
             LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
             WHERE t.user_id = :user_id
             OR t.user_id = ufl.follow_user_id
             """
        ),
        {"user_id": user_id},
    ).fetchall()

    timeline = [
        {"user_id": row["user_id"], "tweet": row["tweet"]} for row in users_rows
    ]

    return jsonify({"user_id": user_id, "timeline": timeline})

    # if user_id not in app.users:
    #     return "사용자가 존재하지 않습니다.", 400

    # follow_list = app.users[user_id].get("follow", set)
    # follow_list.add(user_id)

    # timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]

    return jsonify({"user_id": user_id, "timeline": timeline})
