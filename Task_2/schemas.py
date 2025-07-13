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
        from_attributes = True
        from pydantic import BaseModel

class StudentCreate(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    reading_score: float
    writing_score: float
    math_score: float



from pydantic import BaseModel

class StudentInput(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    reading_score: float
    writing_score: float
    math_score: float



class TestPreparationCreate(BaseModel):
    student_id: int
    status: str

class ExamCreate(BaseModel):
    student_id: int
    math_score: int
    reading_score: int
    writing_score: int
