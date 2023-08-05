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
    
    ## msp 고객 정보 반환 함수
    def customer_auth(self,customer_name):
        auth_list = []
        ## 명명 튜플로 각 고객사 정보 구별
        customer_info = namedtuple('auth_info','customer_name subscription_id subscription_name tenant_id app_id app_key customer_email msp_group appexpire_date msp_class')
        ## 고객사 앱 정보 테이블에 mssql select 쿼리를 통해
        query = f"select * from dbo.customer_auth_info where Customer like '{customer_name}'"
        
        customer_auth_info = self.database_query(query)
        for customer_auth in customer_auth_info:
            info = customer_info._make(customer_auth)
            auth_list.append(info._asdict())
        return auth_list