import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_performance"]

# Drop old collections (keeping exam_audit_log)
db.students.drop()
db.exams.drop()
db.test_preparation_courses.drop()
# Don't drop exam_audit_log to preserve historical audit data

# Load CSV data
csv_path = "C:\\Users\\HP\\Database-Prediction-Pipeline\\StudentsPerformance.csv"
df = pd.read_csv(csv_path)

# Rename columns to match our schema
df = df.rename(columns={
    'race/ethnicity': 'race_ethnicity',
    'parental level of education': 'parental_level_of_education',
    'test preparation course': 'test_preparation_course',
    'math score': 'math_score',
    'reading score': 'reading_score',
    'writing score': 'writing_score'
})

# Insert all students and their data
for index, row in df.iterrows():
    try:
        # Insert student
        student_id = db.students.insert_one({
            "gender": row['gender'],
            "race_ethnicity": row['race_ethnicity'],
            "parental_level_of_education": row['parental_level_of_education'],
            "lunch": row['lunch'],
            "created_at": datetime.now()
        }).inserted_id

        # Insert exam scores
        exam_id = db.exams.insert_one({
            "student_id": student_id,
            "math_score": int(row['math_score']),
            "reading_score": int(row['reading_score']),
            "writing_score": int(row['writing_score']),
            "initial_load": True  # Flag to identify bulk-loaded records
        }).inserted_id

        # Insert test preparation data
        db.test_preparation_courses.insert_one({
            "student_id": student_id,
            "test_preparation_course": row['test_preparation_course']
        })

        # Create initial audit entry for the exam
        db.exam_audit_log.insert_one({
            "exam_id": exam_id,
            "action_type": "CREATE",
            "new_math_score": int(row['math_score']),
            "new_reading_score": int(row['reading_score']),
            "new_writing_score": int(row['writing_score']),
            "changed_at": datetime.now(),
            "changed_by": "system_bulk_load"
        })

        if (index + 1) % 100 == 0:
            print(f"Processed {index + 1} records...")

    except Exception as e:
        print(f"Error processing row {index}: {str(e)}")
        continue

print(f"\nSuccessfully inserted {len(df)} student records with complete audit trails")

# === Exam Audit Log Function ===
def update_exam_score(exam_id, new_math, new_reading, new_writing, changed_by):
    """Updates exam scores and maintains audit trail"""
    exam = db.exams.find_one({"_id": exam_id})
    if not exam:
        print("❌ Exam not found.")
        return False

    # Compare old and new scores
    if (exam["math_score"], exam["reading_score"], exam["writing_score"]) != (new_math, new_reading, new_writing):
        # Update exam
        db.exams.update_one({"_id": exam_id}, {
            "$set": {
                "math_score": new_math,
                "reading_score": new_reading,
                "writing_score": new_writing,
                "last_updated": datetime.now()
            },
            "$unset": {"initial_load": ""}  # Remove bulk load flag
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
        return True
    else:
        print("ℹ️ No changes detected. No update needed.")
        return False

# === Test the audit function ===
print("\nTesting audit functionality...")
sample_exam = db.exams.find_one({"initial_load": True})
if sample_exam:
    print("Updating sample exam:", sample_exam["_id"])
    update_exam_score(
        sample_exam["_id"],
        sample_exam["math_score"] + 5,
        sample_exam["reading_score"] - 2,
        sample_exam["writing_score"] + 1,
        "admin_user"
    )
else:
    print("No bulk-loaded exams found for testing")

# === Aggregation Example ===
print("\n📊 Sample Aggregated Student Performance:")
pipeline = [
    {"$match": {"initial_load": {"$exists": True}}},
    {"$limit": 5}
]

sample_exams = db.exams.aggregate(pipeline)
for exam in sample_exams:
    student = db.students.find_one({"_id": exam["student_id"]})
    prep = db.test_preparation_courses.find_one({"student_id": exam["student_id"]})
    
    print({
        "student_id": str(exam["student_id"]),
        "gender": student["gender"],
        "math": exam["math_score"],
        "reading": exam["reading_score"],
        "writing": exam["writing_score"],
        "test_prep": prep["test_preparation_course"]
    })

print("\n✅ Data load and audit setup completed successfully.")