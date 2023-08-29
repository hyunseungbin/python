home_db = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "port": 3306,
}

DB_URL = f"mysql+mysqlconnector://{home_db['user']}:{home_db['password']}@{home_db['host']}:{home_db['port']}/{home_db['database']}?charset=utf8"
