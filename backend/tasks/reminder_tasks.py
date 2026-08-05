from celery import shared_task
from datetime import date, timedelta

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

    emails_sent = 0

    for job in jobs:

        students = Student.query.filter_by(is_active=True).all()

        for student in students:

            # Branch Eligibility
            if student.branch != job.eligible_branch:
                continue

            # CGPA Eligibility
            if student.cgpa < job.min_cgpa:
                continue

            # Graduation Year Eligibility
            if student.graduation_year != job.eligible_graduation_year:
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

            msg = Message(
                subject="Placement Drive Reminder",
                recipients=[student.user.email]
            )

            msg.body = f"""
Hello {student.full_name},

A placement drive you are eligible for will close tomorrow.

Company : {job.company.company_name}
Role    : {job.title}
Deadline: {job.application_deadline}

Since you satisfy the eligibility criteria, don't miss this opportunity.

Visit the Placement Portal and apply before the deadline.

Regards,
Placement Portal
"""

            mail.send(msg)
            emails_sent += 1

    return f"{emails_sent} reminder emails sent."