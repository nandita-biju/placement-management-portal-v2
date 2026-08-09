from celery import shared_task
from datetime import date, timedelta

from flask import render_template
from flask_mail import Message

from extensions import mail
from models.job import JobPosition
from models.student import Student
from models.application import Application


@shared_task(name="tasks.reminder_tasks.send_daily_reminders")
def send_daily_reminders():
    print("Reminder task running")

    tomorrow = date.today() + timedelta(days=1)

    jobs = JobPosition.query.filter(
        JobPosition.status == "approved",
        JobPosition.application_deadline == tomorrow
    ).all()

    print(f"Found {len(jobs)} job(s) with deadline tomorrow ({tomorrow})")

    emails_sent = 0
    errors = 0

    for job in jobs:

        print(f"Processing job: {job.title} (ID: {job.id}, Branch: {job.eligible_branch}, Deadline: {job.application_deadline})")

        students = Student.query.filter_by(is_active=True).all()

        for student in students:

            # Branch Eligibility (match application route logic)
            if job.eligible_branch and job.eligible_branch.strip().lower() not in ["all", "all branches"]:
                student_branch = (student.branch or "").strip().lower()
                if student_branch != job.eligible_branch.strip().lower():
                    continue

            # CGPA Eligibility
            if job.min_cgpa is not None:
                if student.cgpa is None or float(student.cgpa) < float(job.min_cgpa):
                    continue

            # Graduation Year Eligibility
            if job.eligible_graduation_year is not None:
                if student.graduation_year is None or int(student.graduation_year) != int(job.eligible_graduation_year):
                    continue

            # Already Applied?
            already_applied = Application.query.filter_by(
                student_id=student.id,
                job_id=job.id
            ).first()

            if already_applied:
                continue

            if not student.user:
                continue

            try:
                html = render_template(
                    "reminder_email.html",
                    student_name=student.full_name,
                    company_name=job.company.company_name,
                    job_title=job.title,
                    deadline=job.application_deadline
                )

                msg = Message(
                    subject="Placement Drive Reminder",
                    sender=("Placement Portal", "placementportal217@gmail.com"),
                    recipients=[student.user.email],
                    html=html
                )

                mail.send(msg)
                emails_sent += 1
                print(f"Reminder sent to {student.user.email} for job {job.title}")

            except Exception as e:
                errors += 1
                print(f"ERROR sending to {student.user.email}: {e}")

    return f"{emails_sent} reminder emails sent, {errors} errors."