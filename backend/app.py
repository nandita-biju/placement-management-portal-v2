from flask import Flask
from config import Config
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

from models.student import Student
from models.company import Company
from models.job import JobPosition
from models.application import Application

from routes.student import student_bp
from routes.company import company_bp
from routes.job import job_bp
from routes.application import application_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

    admin_exists = User.query.filter_by(role="admin").first()

    if not admin_exists:
        hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")

        admin = User(
            email="admin@placementportal.com",
            password=hashed_password,
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(company_bp, url_prefix="/company")
app.register_blueprint(job_bp, url_prefix="/jobs")
app.register_blueprint(application_bp, url_prefix="/applications")

@app.route("/")
def home():
    return {"message": "Placement Portal Backend Running"}

if __name__ == "__main__":
    app.run(debug=True)