import json
from app.ml.predict_pipeline import predict_employees

with open("data/raw/test.json") as f:
    data = json.load(f)

results = predict_employees(data)

print(results)
