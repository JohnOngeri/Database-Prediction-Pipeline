from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime
from typing import List, Optional
class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class RaceEthnicityEnum(str, Enum):
    group_a = "group A"
    group_b = "group B"
    group_c = "group C"
    group_d = "group D"
    group_e = "group E"

class EducationEnum(str, Enum):
    some_high_school = "some high school"
    high_school = "high school"
    some_college = "some college"
    associates = "associate's degree"
    bachelors = "bachelor's degree"
    masters = "master's degree"

class LunchEnum(str, Enum):
    standard = "standard"
    free_reduced = "free/reduced"

class PrepStatusEnum(str, Enum):
    completed = "completed"
    none = "none"

class ExamBase(BaseModel):
    math_score: int = Field(..., ge=0, le=100)
    reading_score: int = Field(..., ge=0, le=100)
    writing_score: int = Field(..., ge=0, le=100)

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    student_id: int
    created_at: datetime
    gender: GenderEnum
    race_ethnicity: RaceEthnicityEnum
    parental_level_of_education: EducationEnum
    lunch: LunchEnum
    exams: List[ExamBase] = []
    test_preparation: Optional[PrepStatusEnum] = None

class StudentCreate(StudentBase):
    test_preparation_course: PrepStatusEnum
    math_score: int = Field(..., ge=0, le=100)
    reading_score: int = Field(..., ge=0, le=100)
    writing_score: int = Field(..., ge=0, le=100)

class Student(StudentBase):
    student_id: int
    created_at: datetime
    exams: List[ExamBase] = []
    test_preparation: Optional[PrepStatusEnum] = None

    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    student_id: int
    prediction: float

class PredictionCreate(BaseModel):
    student_id: int
    prediction: float
    prediction_date: datetime

class Prediction(PredictionBase):
    id: int
    prediction_date: datetime

    class Config:
        from_attributes = True