import pandas as pd
import sys
import os
import psycopg2
from dotenv import load_dotenv

model_path = sys.argv[1]
model = pd.read_pickle(model_path)

with open('../data/predict.sql', 'r') as file:
    generate_predict = file.read()

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

print("Predicting...")

create_scoring_table = pd.read_sql_query(generate_predict, connection)

create_scoring_table.drop("total_sales", axis=1, inplace=True)
y_pred = model.predict(create_scoring_table)
create_scoring_table["total_sales"] = y_pred

cursor = connection.cursor()

cursor.execute("DELETE FROM sales_analytics.scoring_ml_antoniovf")
for _, row in create_scoring_table.iterrows():
    try:
        print(f"Updating... \n{row}")
        cursor.execute("INSERT INTO sales_analytics.scoring_ml_antoniovf (store_id, year, month, day, weekday, total_sales) VALUES (%s, %s, %s, %s, %s, %s)", (row["store_id"], row["year"], row["month"], row["day"], row["weekday"], row["total_sales"]))
    except Exception as e:
        print(f"Error updating row: {e}")

connection.commit()
cursor.close()
connection.close()