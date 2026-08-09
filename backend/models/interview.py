from extensions import db
class Interview(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("application.id"),
        nullable=False
    )

    interview_date = db.Column(db.Date, nullable=False)

    interview_time = db.Column(db.Time, nullable=False)

    interview_mode = db.Column(
        db.String(20),
        nullable=False
    )

    interview_location = db.Column(
        db.String(300),
        nullable=False
    )