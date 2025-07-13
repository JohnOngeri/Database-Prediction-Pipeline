from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import StudentInput
import models, schemas, crud
from database import SessionLocal, engine, Base
import pandas as pd
import joblib
import os

# Load model once at the top
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Task 3', 'scripts', 'trained_model.pkl'))
model = joblib.load(MODEL_PATH)


# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# FastAPI app instance
app = FastAPI(title="Student Performance API")
@app.get("/")
def read_root():
    return {"message": "FastAPI is running and connected to MySQL!"}
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def preprocess(data: dict):
    import pandas as pd

    print("🧪 Raw data input to preprocess:", data)

    # Convert to DataFrame
    df = pd.DataFrame([data])
    
    # Explicitly drop unwanted columns
    expected_columns = [
        'gender',
        'race_ethnicity',
        'parental_level_of_education',
        'lunch',
        'reading_score',
        'writing_score',
        'math_score'
    ]
    
    df = df[[col for col in expected_columns if col in df.columns]]

    # Apply mappings
    df['gender'] = df['gender'].map({'male': 0, 'female': 1})
    df['race_ethnicity'] = df['race_ethnicity'].map({
        'black': 0, 'white': 1, 'asian': 2, 'hispanic': 3, 'other': 4
    })
    df['parental_level_of_education'] = df['parental_level_of_education'].map({
        'high school': 0, 'some college': 1, 'associate': 2,
        'university': 3, 'master': 4, 'phd': 5
    })
    df['lunch'] = df['lunch'].map({'standard': 1, 'free/reduced': 0})
    
    return df





@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/", response_model=List[schemas.Student])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Deleted successfully"}
    
  

@app.post("/predict/")
def predict(student: StudentInput):
    try:
        input_data = student.dict()
        X = preprocess(input_data)
        prediction = model.predict(X)[0]
        return {"predicted_target": prediction}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)