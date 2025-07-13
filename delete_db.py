import os

db_path = "students.db"  # adjust this if you stored it elsewhere

try:
    os.remove(db_path)
    print(f"✅ Deleted: {db_path}")
except FileNotFoundError:
    print(f"⚠️ File not found: {db_path}")
except Exception as e:
    print(f"❌ Error deleting {db_path}: {e}")
