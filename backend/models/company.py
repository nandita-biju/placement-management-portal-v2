from extensions import db


class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    company_name = db.Column(db.String(150), nullable=False)

    industry = db.Column(db.String(100))

    location = db.Column(db.String(100))

    website = db.Column(db.String(200))

    approval_status = db.Column(
        db.String(20),
        default="pending"
    )

    user = db.relationship("User", backref="company_profile")