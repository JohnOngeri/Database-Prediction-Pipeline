from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from Task_2.database import Base  

class Student(Base):
    __tablename__ = "Students"
    student_id = Column(Integer, primary_key=True, index=True)
    gender = Column(Enum('male', 'female'))
    race_ethnicity = Column(Enum('group A', 'group B', 'group C', 'group D', 'group E'))
    parental_level_of_education = Column(String(50))
    lunch = Column(Enum('standard', 'free/reduced'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TestPreparation(Base):
    __tablename__ = "TestPreparation"
    prep_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("Students.student_id"))
    status = Column(Enum('completed', 'none'))

class Exam(Base):
    __tablename__ = "Exams"
    exam_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("Students.student_id"))
    math_score = Column(Integer)
    reading_score = Column(Integer)
    writing_score = Column(Integer)
