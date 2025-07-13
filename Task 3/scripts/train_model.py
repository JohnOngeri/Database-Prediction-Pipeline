# train_model.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np


# Step 1: Connect to SQLite DB
engine = create_engine("sqlite:///students.db")
df = pd.read_sql("SELECT * FROM students", engine)

# Step 2: Drop unused columns
if "id" in df.columns:
    df.drop(columns=["id"], inplace=True)

# Step 3: Separate target and features
y = df["math_score"]
X = df.drop(columns=["math_score"])

# Step 4: Preprocessing
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean"))
])

preprocessor = ColumnTransformer([
    ("cat", categorical_pipeline, categorical_cols),
    ("num", numeric_pipeline, numeric_cols)
])

# Step 5: Create training pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Step 6: Train/test split & model fitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Step 7: Evaluate
preds = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))

print(f"✅ Model trained with RMSE: {rmse:.2f}")

# Step 8: Save model
joblib.dump(model, "trained_model.pkl")
print("📦 Model saved to trained_model.pkl")
