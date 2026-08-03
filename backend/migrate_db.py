import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "placement_portal.db")

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check student table columns
    cursor.execute("PRAGMA table_info(student);")
    student_cols = [col[1] for col in cursor.fetchall()]
    
    if "branch" not in student_cols:
        print("Adding branch column to student table...")
        cursor.execute("ALTER TABLE student ADD COLUMN branch VARCHAR(100);")
    
    if "cgpa" not in student_cols:
        print("Adding cgpa column to student table...")
        cursor.execute("ALTER TABLE student ADD COLUMN cgpa FLOAT;")
        
    if "graduation_year" not in student_cols:
        print("Adding graduation_year column to student table...")
        cursor.execute("ALTER TABLE student ADD COLUMN graduation_year INTEGER;")

    # Check job_position table columns
    cursor.execute("PRAGMA table_info(job_position);")
    job_cols = [col[1] for col in cursor.fetchall()]

    if "eligible_branch" not in job_cols:
        print("Adding eligible_branch column to job_position table...")
        cursor.execute("ALTER TABLE job_position ADD COLUMN eligible_branch VARCHAR(100);")

    if "min_cgpa" not in job_cols:
        print("Adding min_cgpa column to job_position table...")
        cursor.execute("ALTER TABLE job_position ADD COLUMN min_cgpa FLOAT;")

    if "eligible_graduation_year" not in job_cols:
        print("Adding eligible_graduation_year column to job_position table...")
        cursor.execute("ALTER TABLE job_position ADD COLUMN eligible_graduation_year INTEGER;")

    if "application_deadline" not in job_cols:
        print("Adding application_deadline column to job_position table...")
        cursor.execute("ALTER TABLE job_position ADD COLUMN application_deadline DATE;")

    conn.commit()
    conn.close()
    print("Database migration completed successfully!")

if __name__ == "__main__":
    migrate()
