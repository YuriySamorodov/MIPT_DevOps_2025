from fastapi import FastAPI
from prometheus_client import make_asgi_app
import uvicorn, random
import sqlite3
from pydantic import BaseModel
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model.pkl')

app = FastAPI(debug=False)
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Pydantic model for prediction input
class PredictionInput(BaseModel):
    time_in_test: int
    VUs: int
    duration: int

@app.get("/")
def read_root(injection: str):
  print(f"Имитация шаблона безопасного SQL-запроса: SELECT * FROM lint WHERE id = ?;")
  print(f"Входной параметр (обрабатывается как данные): {injection}")
  return {"Hello": "World", "received_injection_param": injection}

@app.post("/predict")
def predict(input_data: PredictionInput):
    # Convert input data to pandas DataFrame
    df_input = pd.DataFrame([input_data.dict()])
    
    # Make prediction
    prediction = model.predict(df_input)[0]
    
    return {"predicted_http_req_duration": prediction}
