from celery import shared_task
from flask import render_template
from flask_mail import Message

from extensions import mail, db
from models.user import User
from models.student import Student
from models.company import Company
from models.job import JobPosition
from models.application import Application


@shared_task(name="tasks.report_tasks.send_monthly_report")
def send_monthly_report():

    total_students = Student.query.count()

    total_companies = Company.query.count()

    total_drives = JobPosition.query.count()

    total_applications = Application.query.count()

    shortlisted = Application.query.filter_by(status="Shortlisted").count()

    selected = Application.query.filter_by(status="Selected").count()

    rejected = Application.query.filter_by(status="Rejected").count()

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        return "Admin not found"

    html = render_template(
        "monthly_report.html",
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications,
        shortlisted=shortlisted,
        selected=selected,
        rejected=rejected
    )

    msg = Message(
        subject="Monthly Placement Portal Report",
        recipients=[admin.email],
        html=html
    )

    mail.send(msg)

    return "Monthly report sent."