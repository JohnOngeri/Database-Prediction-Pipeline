from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import StudentData
import models, schemas, crud
from database import SessionLocal, engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

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
def predict(student: StudentData):
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