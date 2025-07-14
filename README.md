 Formative 1: Database - Prediction Pipeline

##  Overview

This project demonstrates an end-to-end pipeline that integrates **relational and NoSQL databases**, **FastAPI**, and **machine learning predictions**. The primary goal is to reinforce database design, implementation, API development, and model integration.

## 👥 Group Members
- John
- Christine
- Nicholas
- Armand

## 📌 Project Structure

```
DATABASE-PREDICTION-PIPELINE/
│
├── models/
│   ├── encoder.pkl
│   ├── feature_names.pkl
│   ├── scaler.pkl
│   ├── student_performance_nn_model.h5
│   └── train_model.py
│
├── Task 1/
│   ├── ERD.png                     # Entity Relationship Diagram
│   ├── insert_sample_data.sql      # SQL file to populate sample data
│   ├── mongo_insert.py             # MongoDB data insertion script
│   └── schema.sql                  # SQL schema with tables, triggers, and procedures
│
├── Task 2/
│   ├── crud.py                     # CRUD operations
│   ├── database.py                 # SQLAlchemy DB connection
│   ├── main.py                     # FastAPI main application
│   ├── models.py                   # Pydantic models and SQLAlchemy models
│   ├── requirements.txt            # Python dependencies
│   ├── reset_db.py                 # Script to reset database
│   └── schemas.py                  # Request/response schemas
│
├── Task 3/
│   ├── predict.py                  # Fetch data and make predictions
│   ├── prediction_pipeline.log     # Log file for predictions
│
├── README.md
└── StudentsPerformance.csv         # Original dataset used
```

---

## 🎯 Objectives

### ✅ Task 1: SQL and MongoDB Setup
- Designed schema with **at least 3 relational tables**
- Created a well-documented **ERD diagram** (`Task 1/ERD.png`)
- Defined **primary and foreign keys**
- Implemented:
  - **Stored Procedure** – to insert validated data
  - **Trigger** – to log changes to exam scores
- Used **MongoDB** to store parallel data using `mongo_insert.py`

### ✅ Task 2: API Endpoints with FastAPI
CRUD operations on the relational database:
- `POST /students` – Create new record
- `GET /students/{id}` – Read record
- `PUT /students/{id}` – Update record
- `DELETE /students/{id}` – Delete record

All API logic is handled in `Task 2/`, powered by **FastAPI** and **SQLAlchemy**.

### ✅ Task 3: Prediction Script
- Used `predict.py` to:
  - Fetch the **latest entry** via the API
  - Preprocess using saved encoder, scaler, and feature list
  - Load pre-trained **Neural Network model** (`.h5`)
  - Make predictions and log output

---

## 📂 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/DATABASE-PREDICTION-PIPELINE.git
cd DATABASE-PREDICTION-PIPELINE
```

### 2. Install Dependencies
Create a virtual environment and install requirements:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r Task\ 2/requirements.txt
```

### 3. Set up the SQL Database
- Run `schema.sql` to create tables, triggers, and stored procedures.
- Insert data using `insert_sample_data.sql`.

### 4. Insert into MongoDB
```bash
python Task\ 1/mongo_insert.py
```

### 5. Run FastAPI Server
```bash
cd Task\ 2
uvicorn main:app --reload
```

### 6. Run Prediction Script
```bash
cd ../Task\ 3
python predict.py
```

---

## 🧪 Model Files
The model is trained using a student performance dataset:
- Preprocessing files: `encoder.pkl`, `scaler.pkl`, `feature_names.pkl`
- Trained Neural Network: `student_performance_nn_model.h5`

Model training logic is found in `models/train_model.py`.

---

## 📉 Sample Dataset
Dataset: `StudentsPerformance.csv`

Source: Kaggle – [“Students Performance in Exams” ](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) 
Contains student scores, gender, test prep course, and demographic data.

---

## 🗂 ERD Diagram

Located at `Task 1/ERD.png`  
(Include a screenshot preview of your ERD here if needed on GitHub)

---

## 📄 Deliverables

- ✅ PDF Report (separate submission)
- ✅ GitHub Repository (this project)
- ✅ Contributions documented in the report

---

## 🙌 Contributions

| Name      | Contributions                                                                 |
|-----------|--------------------------------------------------------------------------------|
| John      | FastAPI CRUD Endpoints, Model Inference Script                                |
| Christine | SQL Schema, Stored Procedure & Trigger, Prediction Pipeline Logging           |
| Nicholas  | MongoDB Integration, ERD Diagram, API Data Fetch                              |
| Armand    | Model Training, Feature Engineering, Requirements Setup                       |


```
