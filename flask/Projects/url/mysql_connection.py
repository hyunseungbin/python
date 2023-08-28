from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)


def create_db_connection():
    connection = mysql.connector.connect(
        host="20.39.197.243",
        user="flask_test",
        password="Strong123@#",
        database="hyuntestdb",
        port="3306",
    )
    return connection


app = Flask(__name__)


@app.route("/")
def index():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
