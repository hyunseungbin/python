from flask import Flask, jsonify, request, render_template
from flask.json import JSONEncoder
import db_config

import mysql.connector


def create_app():
    app = Flask(__name__)
    if db_config is None:
        app.config.from_pyfile("./db_config.py")
    else:
        app.config.update(db_config.db)

    connection = mysql.connector.connect(
        host=app.config["host"],
        user=app.config["user"],
        password=app.config["password"],
        database=app.config["database"],
        port=app.config["port"],
    )
    app.database = connection

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
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)


## 트윗
## http -v POST http://localhost:5000/tweets id:=1 tweet="My first tweet"
@app.route("/tweets", methods=["POST"])
def tweet():
    payloads = request.json
    user_id = int(payloads["id"])
    tweet = payloads["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    if len(tweet) > 300:
        return "300자를 초과하였습니다.", 400

    user_id = int(payloads["id"])

    app.tweets.append({"user_id": user_id, "tweet": tweet})

    return "", 200


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
