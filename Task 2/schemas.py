from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str

class Student(StudentCreate):
    student_id: int
    class Config:
        orm_mode = True

class TestPreparationCreate(BaseModel):
    student_id: int
    status: str

class ExamCreate(BaseModel):
    student_id: int
    math_score: int
    reading_score: int
    writing_score: int
