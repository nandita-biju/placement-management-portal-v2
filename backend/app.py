import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import JWTManager
from celery_utils import make_celery

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
from routes.admin import admin_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

celery_app = make_celery(app)

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
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def home():
    return {"message": "Placement Portal Backend Running"}

@app.route("/exports/<path:filename>", methods=["GET"])
def download_export(filename):
    exports_dir = os.path.join(app.root_path, "exports")
    return send_from_directory(exports_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
