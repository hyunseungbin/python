from sqlalchemy import create_engine, text

office_db = {
    "host": "20.39.197.243",
    "user": "flask_test",
    "password": "Strong123!",
    "database": "hyuntestdb",
    "port": 3306,
}
home_db = {
    "host": "20.39.197.243",
    "user": "office",
    "password": "Strongpassword123!",
    "database": "hyuntestdb",
    "port": 3306,
}

DB_URL = f"mysql+mysqlconnector://{home_db['user']}:{home_db['password']}@{home_db['host']}:{home_db['port']}/{home_db['database']}?charset=utf8"
D = f"mysql+mysqlconnector://{office_db['user']}:{office_db['password']}@{office_db['host']}:{office_db['port']}/{office_db['database']}?charset=utf8"

# params = {"name": "현승빈"}
# rows = db_conn.execute(
#     text("SELECT * FROM users_profile WHERE name = :name"), params
# ).fetchall()

# for row in rows:
#     print(row["name"])
