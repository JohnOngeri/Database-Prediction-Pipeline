# predict.py
import requests
import pandas as pd
import joblib

# Step 1: Fetch the latest record from the FastAPI endpoint
API_URL = "http://127.0.0.1:8000/students/latest"  # Adjust if different
response = requests.get(API_URL)

if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

latest_record = response.json()

# Step 2: Convert to DataFrame
df = pd.DataFrame([latest_record])

# Keep a copy of actual math score if it exists (to compare)
actual_math_score = df.get("math_score", None)
if "id" in df:
    df.drop("id", axis=1, inplace=True)
if "math_score" in df:
    df.drop("math_score", axis=1, inplace=True)

# Step 3: Load the model
model = joblib.load("models/trained_model.pkl")

# Step 4: Predict
prediction = model.predict(df)
predicted_value = prediction[0]

# Step 5: Output
print("Student Info:", df.to_dict(orient='records')[0])
if actual_math_score is not None:
    print(f"Actual Math Score: {actual_math_score.values[0]}")
print(f"🔮 Predicted Math Score: {predicted_value:.2f}")
