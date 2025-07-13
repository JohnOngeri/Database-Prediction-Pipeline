from sqlalchemy.orm import Session
import models, schemas 

# STUDENTS
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session):
    return db.query(models.Student).all()

def update_student(db: Session, student_id: int, updates: schemas.StudentCreate):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student:
        for field, value in updates.dict().items():
            setattr(student, field, value)
        db.commit()
        db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student
