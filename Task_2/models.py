from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    race_ethnicity = Column(String)
    parental_level_of_education = Column(String)
    lunch = Column(String)
    test_preparation_course = Column(String)
    math_score = Column(Integer)
    reading_score = Column(Integer)
    writing_score = Column(Integer)
    
class TestPreparation(Base):
    __tablename__ = "TestPreparation"
    prep_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(Enum('completed', 'none'))

class Exam(Base):
    __tablename__ = "Exams"
    exam_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    math_score = Column(Integer)
    reading_score = Column(Integer)
    writing_score = Column(Integer)
