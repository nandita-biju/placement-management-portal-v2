from extensions import db


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    full_name = db.Column(db.String(100), nullable=False)

    education = db.Column(db.String(200))

    skills = db.Column(db.Text)

    resume_link = db.Column(db.String(300))

    experience = db.Column(db.Text)

    user = db.relationship("User", backref="student_profile")