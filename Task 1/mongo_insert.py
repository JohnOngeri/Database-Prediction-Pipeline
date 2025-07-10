from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_performance"]

# Drop old collections
db.students.drop()
db.exams.drop()
db.test_preparation_courses.drop()
db.exam_audit_log.drop()

# === 1. Insert Students ===
students = db.students

student1 = students.insert_one({
    "gender": "female",
    "race_ethnicity": "group B",
    "parental_level_of_education": "bachelor’s degree",
    "lunch": "standard",
    "created_at": datetime.now()
}).inserted_id

student2 = students.insert_one({
    "gender": "female",
    "race_ethnicity": "group C",
    "parental_level_of_education": "some college",
    "lunch": "standard",
    "created_at": datetime.now()
}).inserted_id

student3 = students.insert_one({
    "gender": "female",
    "race_ethnicity": "group B",
    "parental_level_of_education": "master’s degree",
    "lunch": "standard",
    "created_at": datetime.now()
}).inserted_id

# === 2. Insert Exams ===
exams = db.exams

exam1 = exams.insert_one({
    "student_id": student1,
    "math_score": 72,
    "reading_score": 72,
    "writing_score": 74
}).inserted_id

exam2 = exams.insert_one({
    "student_id": student2,
    "math_score": 69,
    "reading_score": 90,
    "writing_score": 88
}).inserted_id

exam3 = exams.insert_one({
    "student_id": student3,
    "math_score": 90,
    "reading_score": 95,
    "writing_score": 93
}).inserted_id

# === 3. Insert Test Preparation Data ===
test_prep = db.test_preparation_courses

test_prep.insert_many([
    {"student_id": student1, "test_preparation_course": "none"},
    {"student_id": student2, "test_preparation_course": "completed"},
    {"student_id": student3, "test_preparation_course": "none"}
])

# === 4. Exam Audit Log Function ===
def update_exam_score(exam_id, new_math, new_reading, new_writing, changed_by):
    exam = exams.find_one({"_id": exam_id})
    if not exam:
        print("❌ Exam not found.")
        return

    # Compare old and new
    if (exam["math_score"], exam["reading_score"], exam["writing_score"]) != (new_math, new_reading, new_writing):
        # Update exam
        exams.update_one({"_id": exam_id}, {
            "$set": {
                "math_score": new_math,
                "reading_score": new_reading,
                "writing_score": new_writing
            }
        })

        # Log change
        db.exam_audit_log.insert_one({
            "exam_id": exam_id,
            "action_type": "UPDATE",
            "old_math_score": exam["math_score"],
            "new_math_score": new_math,
            "old_reading_score": exam["reading_score"],
            "new_reading_score": new_reading,
            "old_writing_score": exam["writing_score"],
            "new_writing_score": new_writing,
            "changed_at": datetime.now(),
            "changed_by": changed_by
        })
        print("✅ Exam updated and logged.")
    else:
        print("ℹ️ No changes detected. No update needed.")

# Example update call:
update_exam_score(exam2, 75, 90, 88, "admin_user")

# === 5. Aggregation: Join Students + Exams + Prep ===
print("\n📊 Aggregated Student Performance:")
pipeline = [
    {
        "$lookup": {
            "from": "exams",
            "localField": "_id",
            "foreignField": "student_id",
            "as": "exam_scores"
        }
    },
    {
        "$lookup": {
            "from": "test_preparation_courses",
            "localField": "_id",
            "foreignField": "student_id",
            "as": "test_prep"
        }
    },
    {
        "$unwind": "$exam_scores"
    },
    {
        "$unwind": "$test_prep"
    },
    {
        "$project": {
            "_id": 0,
            "gender": 1,
            "race_ethnicity": 1,
            "parental_level_of_education": 1,
            "math_score": "$exam_scores.math_score",
            "reading_score": "$exam_scores.reading_score",
            "writing_score": "$exam_scores.writing_score",
            "test_preparation_course": "$test_prep.test_preparation_course"
        }
    }
]

results = db.students.aggregate(pipeline)
for doc in results:
    print(doc)

print("\n✅ Script completed successfully.")
