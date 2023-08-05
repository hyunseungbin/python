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
    
    def app_auth_info(self,query):
        auth_list = []
        ## 명명 튜플로 각 고객사 정보 구별
        app_info = namedtuple('auth_info','subscription_id subscription_name tenant_id app_id app_key')
        ## 고객사 앱 정보 테이블에 mssql select 쿼리를 통해
        
        app_auth_info = self.database_query(query)
        for app_auth in app_auth_info:
            info = app_info._make(app_auth)
            auth_list.append(info._asdict())
        return auth_list