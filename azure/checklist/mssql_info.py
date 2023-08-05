import pymssql
import json
from collections import namedtuple
file_path ='.\Azure\db_account_info.json'

class mssql:
    def __init__(self):
        with open(file_path, 'r') as f:
            db_info = json.load(f)
        # 데이터베이스 연결 설정
        self.server = db_info['server']
        self.database = db_info['database']
        self.username = db_info['username']
        self.password = db_info['password']
    
    def database_query(self,query):
        # db_account_info.json 파일 읽어오기
        cnxn = pymssql.connect(self.server, self.username, self.password, self.database)
        cursor = cnxn.cursor()
        ## 기존 데이터 삭제 
        cursor.execute(query)
        query_data = cursor.fetchall()

        return query_data
    