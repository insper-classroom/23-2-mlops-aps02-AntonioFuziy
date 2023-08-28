import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

with open('../data/train.sql', 'r') as file:
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

df = pd.read_sql_query(sql_query, connection)

connection.close()

today = datetime.now().date()

df.to_parquet(f"../data/train-{today}.parquet")