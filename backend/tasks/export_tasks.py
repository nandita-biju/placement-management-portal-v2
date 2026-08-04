import csv
import os
from celery import shared_task
from models.student import Student
from models.application import Application

@shared_task(name="tasks.export_tasks.export_student_applications")
def export_student_applications(student_id):
    student = Student.query.get(student_id)
    student_name = student.full_name if student else "Unknown"

    applications = Application.query.filter_by(student_id=student_id).all()

    # Base directory for backend
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exports_dir = os.path.join(backend_dir, "exports")
    os.makedirs(exports_dir, exist_ok=True)

    filename = f"applications_{student_id}.csv"
    filepath = os.path.join(exports_dir, filename)

    headers = [
        "Student Name",
        "Company Name",
        "Drive Title",
        "Application Status",
        "Applied Date"
    ]

    with open(filepath, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        for app in applications:
            company_name = app.job.company.company_name if (app.job and app.job.company) else "N/A"
            drive_title = app.job.title if app.job else "N/A"
            applied_date = app.applied_at.strftime("%Y-%m-%d %H:%M:%S") if app.applied_at else ""

            writer.writerow([
                student_name,
                company_name,
                drive_title,
                app.status,
                applied_date
            ])

    return filename
