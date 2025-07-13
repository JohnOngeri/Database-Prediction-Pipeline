from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_db import Student, Base

# Use the same DB path as in init_db.py
DATABASE_URL = "sqlite:///../students.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Define dummy student records
students = [
    Student(
        gender="male",
        race_ethnicity="group A",
        parental_level_of_education="bachelor's degree",
        lunch="standard",
        reading_score=72,
        writing_score=74,
        math_score=70
    ),
    Student(
        gender="female",
        race_ethnicity="group B",
        parental_level_of_education="some college",
        lunch="free/reduced",
        reading_score=88,
        writing_score=90,
        math_score=85
    ),
    Student(
        gender="female",
        race_ethnicity="group C",
        parental_level_of_education="associate's degree",
        lunch="standard",
        reading_score=95,
        writing_score=93,
        math_score=97
    )
]

# Insert and commit
session.add_all(students)
session.commit()
session.close()

print("✅ Dummy data inserted successfully.")
