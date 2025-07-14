from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from crud import *
from schemas import *
import logging
import os
import models
from sqlalchemy.orm import joinedload
from requests import post
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Student Performance API",
    description="API for managing student performance data",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
@app.on_event("startup")
def startup_event():
    if os.getenv("ENVIRONMENT") == "development":
        Base.metadata.drop_all(bind=engine)
        logger.warning("Dropped all tables (development mode)")
    
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized")

# Health check endpoint
@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "message": "Student Performance API is running"}

# Student endpoints
@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return create_student_with_exam(db, student)
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def read_student(student_id: int, db: Session = Depends(get_db)):
    # Get student with all relationships
    db_student = (
        db.query(models.Student)
        .options(
            joinedload(models.Student.exams),
            joinedload(models.Student.test_preparation)
        )
        .filter(models.Student.student_id == student_id)
        .first()
    )
    
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Prepare the test preparation status
    prep_status = None
    if db_student.test_preparation:
        prep_status = "completed" if db_student.test_preparation else "none"
    
    return {
        "student_id": db_student.student_id,
        "gender": db_student.gender,
        "race_ethnicity": db_student.race_ethnicity,
        "parental_level_of_education": db_student.parental_level_of_education,
        "lunch": db_student.lunch,
        "created_at": db_student.created_at,
        "exams": db_student.exams,  # This will be a list
        "test_preparation": prep_status  # Single value
    }

@app.get("/students/", response_model=list[Student], tags=["Students"])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_students(db, skip=skip, limit=limit)

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not delete_student(db, student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return {"message": "Student deleted successfully"}

@app.get("/students/latest/", response_model=StudentBase)
def read_latest_student(db: Session = Depends(get_db)):
    student = get_latest_student(db)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No students found"
        )

    # Get the exams and test preparation status
    exams = [{"math_score": exam.math_score, "reading_score": exam.reading_score, "writing_score": exam.writing_score} for exam in student.exams]
    test_preparation_status = student.test_preparation.status if student.test_preparation else None


    # Return the student data with additional fields
    return {
        "student_id": student.student_id,
        "gender": student.gender,
        "race_ethnicity": student.race_ethnicity,
        "parental_level_of_education": student.parental_level_of_education,
        "lunch": student.lunch,
        "created_at": student.created_at,
        "exams": exams,
        "test_preparation": test_preparation_status
    }
# Prediction endpoints
@app.post("/predictions/", response_model=Prediction, tags=["Predictions"])
def create_prediction(
    prediction: PredictionCreate, 
    db: Session = Depends(get_db)
):
    try:
        # Create and save the prediction directly
        db_prediction = models.Prediction(
            student_id=prediction.student_id,
            prediction=prediction.prediction,
            prediction_date=datetime.utcnow()
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return db_prediction
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid request data: {str(e)}"
        )