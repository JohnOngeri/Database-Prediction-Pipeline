from pymongo import MongoClient

# Connect to local MongoDB or Atlas connection string
client = MongoClient("mongodb://localhost:27017")
db = client["student_performance"]

# Students
students = db.students
student1 = students.insert_one({
    "gender": "female",
    "parental_level_of_education": "bachelor’s degree"
}).inserted_id

student2 = students.insert_one({
    "gender": "male",
    "parental_level_of_education": "some college"
}).inserted_id

student3 = students.insert_one({
    "gender": "female",
    "parental_level_of_education": "high school"
}).inserted_id

# Exams
db.exams.insert_many([
    {
        "student_id": student1,
        "math_score": 72,
        "reading_score": 72,
        "writing_score": 74
    },
    {
        "student_id": student2,
        "math_score": 69,
        "reading_score": 90,
        "writing_score": 88
    },
    {
        "student_id": student3,
        "math_score": 90,
        "reading_score": 95,
        "writing_score": 93
    }
])

# Test Preparation Courses
db.test_preparation_courses.insert_many([
    {
        "student_id": student1,
        "test_preparation_course": "none"
    },
    {
        "student_id": student2,
        "test_preparation_course": "completed"
    },
    {
        "student_id": student3,
        "test_preparation_course": "completed"
    }
])

print("Data inserted successfully into MongoDB!")
