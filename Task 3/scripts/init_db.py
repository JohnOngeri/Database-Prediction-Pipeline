from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

DATABASE_URL = "sqlite:///../students.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    race_ethnicity = Column(String)
    parental_level_of_education = Column(String)
    lunch = Column(String)
    reading_score = Column(Integer)
    writing_score = Column(Integer)
    math_score = Column(Integer)

Base.metadata.create_all(bind=engine)
print("✅ Database and 'students' table created successfully.")
