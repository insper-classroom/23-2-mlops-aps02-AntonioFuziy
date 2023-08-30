from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime
import os
from dotenv import load_dotenv
import psycopg2

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

df = pd.read_sql_query("SELECT store_id, year, month, day, weekday, total_sales FROM sales_analytics.view_abt_train_antoniovf;", connection)

X = df.drop("total_sales", axis=1)
y = df["total_sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1912)

print("Training model...")

model = RandomForestRegressor(n_estimators=100, random_state=195)
model.fit(X_train, y_train)

today = datetime.now().date()

model_file_path = f"../models/model-{today}.pkl"

print(f"Saving to {model_file_path}...")

with open(model_file_path, "wb") as f:
  pickle.dump(model, f)