from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime, CheckConstraint  # Added CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    gender = Column(Enum('male', 'female', name='gender_enum'), nullable=False)
    race_ethnicity = Column(Enum('group A', 'group B', 'group C', 'group D', 'group E', name='race_enum'), nullable=False)
    parental_level_of_education = Column(Enum(
        'some high school', 'high school', 'some college',
        'associate\'s degree', 'bachelor\'s degree', 'master\'s degree',
        name='education_enum'
    ), nullable=False)
    lunch = Column(Enum('standard', 'free/reduced', name='lunch_enum'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    test_preparation = relationship("TestPreparation", back_populates="student", uselist=False, cascade="all, delete")
    exams = relationship("Exam", back_populates="student", cascade="all, delete")
    predictions = relationship("Prediction", back_populates="student")

class TestPreparation(Base):
    __tablename__ = "test_preparation"
    
    prep_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    status = Column(Enum('completed', 'none', name='prep_status_enum'), nullable=False)
    
    student = relationship("Student", back_populates="test_preparation")

class Exam(Base):
    __tablename__ = "exams"
    
    exam_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    math_score = Column(Integer, CheckConstraint("math_score BETWEEN 0 AND 100"))
    reading_score = Column(Integer, CheckConstraint("reading_score BETWEEN 0 AND 100"))
    writing_score = Column(Integer, CheckConstraint("writing_score BETWEEN 0 AND 100"))
    
    student = relationship("Student", back_populates="exams")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    prediction = Column(Float)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    student = relationship("Student", back_populates="predictions")