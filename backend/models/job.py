from extensions import db


class JobPosition(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.id"),
        nullable=False
    )

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    salary = db.Column(db.String(50))

    skills_required = db.Column(db.Text)

    eligible_branch = db.Column(db.String(100))

    min_cgpa = db.Column(db.Float)

    eligible_graduation_year = db.Column(db.Integer)

    application_deadline = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    company = db.relationship("Company", backref="jobs")