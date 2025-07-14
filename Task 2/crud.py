from sqlalchemy.orm import Session
from models import Student, TestPreparation, Exam, Prediction
import schemas
from schemas import PrepStatusEnum
def create_student_with_exam(db: Session, student: schemas.StudentCreate):
    db_student = Student(
        gender=student.gender.value,
        race_ethnicity=student.race_ethnicity.value,
        parental_level_of_education=student.parental_level_of_education.value,
        lunch=student.lunch.value
    )
    db.add(db_student)
    db.flush()  # Get the student_id before commit
    
    db.add(TestPreparation(
        student_id=db_student.student_id,
        status=student.test_preparation_course.value
    ))
    
    db.add(Exam(
        student_id=db_student.student_id,
        math_score=student.math_score,
        reading_score=student.reading_score,
        writing_score=student.writing_score
    ))
    
    db.commit()
    test_preparation_status = "completed" if student.test_preparation_course == PrepStatusEnum.completed else "none"
    
    return {
        "student_id": db_student.student_id,
        "gender": db_student.gender,
        "race_ethnicity": db_student.race_ethnicity,
        "parental_level_of_education": db_student.parental_level_of_education,
        "lunch": db_student.lunch,
        "created_at": db_student.created_at,
        "exams": [{
        "math_score": student.math_score,
        "reading_score": student.reading_score,
        "writing_score": student.writing_score
    }],
        "test_preparation": test_preparation_status  # Single value
    }
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.student_id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

def create_prediction(db: Session, prediction: schemas.PredictionCreate):
    db_prediction = Prediction(**prediction.model_dump())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_latest_student(db: Session):
    return db.query(Student).order_by(Student.student_id.desc()).first()