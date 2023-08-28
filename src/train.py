from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import sys
from datetime import datetime

df_path = sys.argv[-1] 

df = pd.read_parquet(df_path)

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