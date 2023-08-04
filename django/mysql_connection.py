## 해당 mysql에 모듈이 없을 경우
## pip install mysql-connector-python

import mysql.connector

## MySQL 연결
connection = mysql.connector.connect(
    host='20.39.197.243',
    user='python_hyun',
    password='StrongPass123@',
    database='hyuntestdb',
    port='3306'
)

## cursor 개체만들기
table_name = 'resource'
cursor = connection.cursor()
delete_query = f"DROP TABLE {table_name};"
create_query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, resource_type VARCHAR(255) );"
select_query = f"SELECT * FROM {table_name}"
resource_type_list = ['virtual_machine', 'networks', 'database', 'vpn', 'application_gateway','storage_account']
cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
table_exists = cursor.fetchone()
if table_exists != None:
    cursor.execute(delete_query)
    results = cursor.fetchall()

cursor.execute(create_query)
results = cursor.fetchall()
print(results)

#'users' 테이블에서 모든 행 가져오기
# Check if the table exists
# cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
# table_exists = cursor.fetchone()
# if table_exists == None:
#     cursor.execute(create_query)
#     results = cursor.fetchall()
#     print(results)
# insert_query = f"DESCRIBE {table_name};"
# cursor.execute(insert_query)




for resource_type in resource_type_list:
    insert_query = f"INSERT INTO {table_name} (resource_type) VALUES ('{resource_type}');"
    cursor.execute(insert_query)
    print(cursor,cursor.fetchall())

flush = "FLUSH PRIVILEGES;"
cursor.execute(flush)
# cursor.execute(insert_query)
# results = cursor.fetchall()
# # Fetch the results
# print(results)

cursor.execute(select_query)
results = cursor.fetchall()
# Fetch the results
print(results)



# Process the results (e.g., print them)
# for row in results:
#     print(row)
    
    
#INSERT INTO users (id, name) VALUES (1, 'user_name');
