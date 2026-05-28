from extensions import db
from datetime import datetime


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job_position.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Applied"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship("Student", backref="applications")

    job = db.relationship("JobPosition", backref="applications")