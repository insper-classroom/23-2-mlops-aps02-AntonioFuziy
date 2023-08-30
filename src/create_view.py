import os
from dotenv import load_dotenv
import psycopg2

with open('../data/create_view.sql', 'r') as file:
    sql_query = file.read()

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_DATABASE")

connection = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    dbname=db_name
)

cursor = connection.cursor()
cursor.execute(sql_query)
connection.commit()

cursor.close()
connection.close()