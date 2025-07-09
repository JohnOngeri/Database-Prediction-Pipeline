# 🧠 Student Performance Database & API Project

## 📌 Overview

This project is part of our Database and API Integration assignment. It focuses on:

- Designing and implementing a relational database (MySQL) and NoSQL database (MongoDB)
- Creating FastAPI CRUD endpoints for relational DB operations
- Building a script to fetch and prepare data for ML predictions

We use the **"Students Performance in Exams"** dataset from Kaggle:  
🔗 [Dataset Link](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)

---

## 🗃️ Folder Structure

```
student-performance-db-api/
│
├── schema.sql                  # SQL script to create and populate MySQL tables
├── README.md                   # This file
│
├── api/                        # FastAPI backend
│   ├── main.py                 # FastAPI app with CRUD endpoints
│   └── db_config.py            # MySQL connection config (optional)
│
├── prediction_script/          # ML prediction script
│   └── predict.py              # Fetches latest data via API and makes prediction
│
├── models/                     # ML model (optional)
│   └── trained_model.pkl       # Pre-trained model for prediction
│
└── docs/                       # Documents and diagrams
    ├── ERD_Diagram.png         # Entity-Relationship Diagram (ERD)
    └── Assignment_Report.pdf   # Final report with team contributions
```

---

## ⚙️ How to Run

### 1. 💾 MySQL Setup

- Open MySQL Workbench
- Run `schema.sql` to create and populate the database

### 2. 🚀 FastAPI Setup

```bash
# Navigate to the api folder
cd api

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install fastapi uvicorn mysql-connector-python

# Run FastAPI server
uvicorn main:app --reload
```

### 3. 🔍 ML Prediction Script

```bash
# Navigate to prediction_script folder
cd prediction_script

# Install required packages
pip install pandas scikit-learn requests joblib

# Run prediction script
python predict.py
```

---

## 👥 Team Members & Contributions

| Name       | Contribution                                          |
|------------|-------------------------------------------------------|
| Christine  | MongoDB implementation and NoSQL schema               |
| John       | SQL schema creation, ERD design, GitHub setup         |
| Armand     | FastAPI CRUD endpoints and API logic                  |
| Nicholas   | ML model integration and prediction script development|

---

## 📎 Report & Diagrams

See [`/docs/Assignment_Report.pdf`](docs/Assignment_Report.pdf) for:
- ERD Diagram
- Implementation screenshots
- Team member contributions
- GitHub link to repository

---

