import pymysql
from database import DATABASE_URL

#Extract database info from URL
db_info = DATABASE_URL.split('://')[1].split('@')
user_pass, host_db = db_info[0].split(':'), db_info[1].split('/')
username, password = user_pass[0], user_pass[1]
host, db_name = host_db[0], host_db[1]

# Connect and recreate database
connection = pymysql.connect(
    host=host,
    user=username,
    password=password
)

try:
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} recreated successfully")
    connection.commit()
finally:
    connection.close()