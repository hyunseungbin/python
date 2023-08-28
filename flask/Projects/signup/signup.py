from flask import Flask, render_template, request, redirect, jsonify

import mysql.connector

app = Flask(__name__)

# Database connection function (create_db_connection)


@app.route("/")
def index():
    return render_template("signup.html")


# ## flask 에서 set을 json으로 바꾸는 클래스
# class CustomerJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, set):
#             return list(obj)

#         return JSONEncoder.default(self, obj)


# app.json_encoder = CustomerJSONEncoder


def create_db_connection():
    connection = mysql.connector.connect(
        host="20.39.197.243",
        user="flask_test",
        password="Strong123@#",
        database="hyuntestdb",
        port="3306",
    )
    return connection


# @app.route("/")
# def index():
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM test_users")
#     data = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return render_template("index.html", data=data)


# ... Database connection function (create_db_connection) ...


@app.route("/add_data", methods=["POST"])
def add_data():
    if request.method == "POST":
        new_user = request.json

        connection = create_db_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO test_users (name, age) VALUES (%s, %s)"
        data = (name, age)

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")  # Redirect back to the main page


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO test_users (name, age) VALUES (%s, %s)", (name, age)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return "Data inserted successfully!"


if __name__ == "__main__":
    app.run(debug=True)
