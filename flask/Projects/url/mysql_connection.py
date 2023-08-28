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


from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ... Database connection function (create_db_connection) ...


@app.route("/add_data", methods=["POST"])
def add_data():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")

        connection = create_db_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO test_users (name, age) VALUES (%s, %s)"
        data = (name, age)

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")  # Redirect back to the main page


if __name__ == "__main__":
    app.run(debug=True)
