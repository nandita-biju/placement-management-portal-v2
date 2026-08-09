import os
import uuid

from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from extensions import cache
from sqlalchemy.orm import joinedload

from models.job import JobPosition
from models.application import Application
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.user import User
from models.student import Student
from models.company import Company


student_bp = Blueprint("student", __name__)

ALLOWED_RESUME_EXTENSIONS = {"pdf"}
def allowed_resume(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_RESUME_EXTENSIONS
    )

@student_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_student_profile():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    existing_profile = Student.query.filter_by(
        user_id=user_id
    ).first()

    if existing_profile:
        return jsonify({
            "message": "Profile already exists"
        }), 400

    data = request.get_json()

    profile = Student(
        user_id=user_id,
        full_name=data["full_name"],
        education=data.get("education"),
        skills=data.get("skills"),
        resume_link=data.get("resume_link"),
        experience=data.get("experience"),
        branch=data.get("branch"),
        cgpa=float(data["cgpa"]) if data.get("cgpa") is not None and data.get("cgpa") != "" else None,
        graduation_year=int(data["graduation_year"]) if data.get("graduation_year") is not None and data.get("graduation_year") != "" else None
    )

    db.session.add(profile)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Student profile created successfully"
    }), 201

def student_profile_cache_key():
    user_id = get_jwt_identity()

    return f"student-profile:{user_id}"

@student_bp.route("/profile", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, make_cache_key=student_profile_cache_key)
def get_student_profile():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    profile = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Profile not found"
        }), 404

    return jsonify({
        "full_name": profile.full_name,
        "education": profile.education,
        "skills": profile.skills,
        "resume_link": profile.resume_link,
        "experience": profile.experience,
        "branch": profile.branch,
        "cgpa": profile.cgpa,
        "graduation_year": profile.graduation_year
    }), 200

@student_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    data = request.get_json()

    student.full_name = data["full_name"]
    student.education = data.get("education")
    student.skills = data.get("skills")
    student.experience = data.get("experience")
    student.branch = data.get("branch")
    student.cgpa = float(data["cgpa"]) if data.get("cgpa") is not None and data.get("cgpa") != "" else None
    student.graduation_year = int(data["graduation_year"]) if data.get("graduation_year") is not None and data.get("graduation_year") != "" else None

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200
    
@student_bp.route("/drives", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def get_all_drives():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    jobs = (
        JobPosition.query
        .options(joinedload(JobPosition.company))
        .filter_by(status="approved")
        .all()
    )

    output = []

    for job in jobs:
        output.append({
            "id": job.id,
            "company_id": job.company.id,
            "company_name": job.company.company_name,
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "skills_required": job.skills_required,
            "eligible_branch": job.eligible_branch,
            "min_cgpa": job.min_cgpa,
            "eligible_graduation_year": job.eligible_graduation_year,
            "application_deadline": job.application_deadline.strftime("%Y-%m-%d") if job.application_deadline else None,
            "status": job.status
        })
    return jsonify(output), 200

@student_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student_by_id(student_id):

    claims = get_jwt()

    if claims["role"] not in ["company", "admin"]:
        return jsonify({
            "message":"Access denied"
        }),403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message":"Student not found"
        }),404

    return jsonify({

        "id":student.id,
        "full_name":student.full_name,
        "education":student.education,
        "skills":student.skills,
        "experience":student.experience,
        "resume_link":student.resume_link,
        "branch":student.branch,
        "cgpa":student.cgpa,
        "graduation_year":student.graduation_year

    }),200

from celery.result import AsyncResult
from tasks.export_tasks import export_student_applications

@student_bp.route("/export-applications", methods=["POST"])
@jwt_required()
def trigger_export_applications():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    # Trigger Celery task
    task = export_student_applications.delay(student.id)

    return jsonify({
        "message": "Export started successfully",
        "task_id": task.id
    }), 202

@student_bp.route("/export-status/<task_id>", methods=["GET"])
@jwt_required()
def get_export_status(task_id):

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    res = AsyncResult(task_id)

    if res.state in ["PENDING", "STARTED", "RETRY"]:
        return jsonify({
            "status": "Processing"
        }), 200

    elif res.state == "SUCCESS":
        filename = res.result if isinstance(res.result, str) else f"applications_{get_jwt_identity()}.csv"
        return jsonify({
            "status": "Completed",
            "download_url": f"/exports/{filename}"
        }), 200

    else:
        return jsonify({
            "status": "Failed"
        }), 200

@student_bp.route("/profile/resume", methods=["POST"])
@jwt_required()
def upload_resume():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    if "resume" not in request.files:
        return jsonify({
            "message": "No resume file provided"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "No file selected"
        }), 400

    if not allowed_resume(file.filename):
        return jsonify({
            "message": "Only PDF resumes are allowed"
        }), 400

    upload_folder = os.path.join(
        current_app.root_path,
        "uploads",
        "resumes"
    )

    os.makedirs(upload_folder, exist_ok=True)

    # Delete old resume if it exists
    if student.resume_link:

        old_file = os.path.join(
            upload_folder,
            student.resume_link
        )

        if os.path.exists(old_file):
            os.remove(old_file)

    original_filename = secure_filename(file.filename)

    unique_filename = (
        str(uuid.uuid4())
        + "_"
        + original_filename
    )

    file_path = os.path.join(
        upload_folder,
        unique_filename
    )

    file.save(file_path)

    student.resume_link = unique_filename

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": unique_filename
    }), 200

@student_bp.route("/profile/resume", methods=["GET"])
@jwt_required()
def view_my_resume():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    if not student.resume_link:
        return jsonify({
            "message": "Resume not uploaded"
        }), 404

    upload_folder = os.path.join(
        current_app.root_path,
        "uploads",
        "resumes"
    )

    file_path = os.path.join(
        upload_folder,
        student.resume_link
    )

    if not os.path.exists(file_path):
        return jsonify({
            "message": "Resume file not found"
        }), 404

    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=False
    )

@student_bp.route("/profile/resume", methods=["DELETE"])
@jwt_required()
def delete_resume():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    if not student.resume_link:
        return jsonify({
            "message": "No resume to delete"
        }), 404

    upload_folder = os.path.join(
        current_app.root_path,
        "uploads",
        "resumes"
    )

    file_path = os.path.join(
        upload_folder,
        student.resume_link
    )

    # Prevent path traversal
    real_upload = os.path.realpath(upload_folder)
    real_file = os.path.realpath(file_path)

    if not real_file.startswith(real_upload):
        return jsonify({
            "message": "Invalid file path"
        }), 400

    if os.path.exists(real_file):
        os.remove(real_file)

    student.resume_link = None

    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Resume deleted successfully"
    }), 200

@student_bp.route(
    "/student/<int:student_id>/resume",
    methods=["GET"]
)
@jwt_required()
def view_student_resume(student_id):

    claims = get_jwt()

    if claims["role"] not in ["company", "admin"]:
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    # If company is viewing the resume,
    # make sure the student actually applied
    # to one of that company's drives.

    if claims["role"] == "company":

        company_user_id = int(get_jwt_identity())

        company = Company.query.filter_by(
            user_id=company_user_id
        ).first()

        if not company:
            return jsonify({
                "message": "Company profile not found"
            }), 404

        application = (
            Application.query
            .join(JobPosition, Application.job_id == JobPosition.id)
            .filter(
                Application.student_id == student_id,
                JobPosition.company_id == company.id
            )
            .first()
        )

        if not application:
            return jsonify({
                "message": "You are not authorized to view this resume"
            }), 403

    if not student.resume_link:
        return jsonify({
            "message": "Resume not uploaded"
        }), 404

    upload_folder = os.path.join(
        current_app.root_path,
        "uploads",
        "resumes"
    )

    file_path = os.path.join(
        upload_folder,
        student.resume_link
    )

    if not os.path.exists(file_path):
        return jsonify({
            "message": "Resume file not found"
        }), 404

    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=False
    )

@student_bp.route("/interviews", methods=["GET"])
@jwt_required()
def get_my_interviews():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    applications = Application.query.filter_by(
        student_id=student.id,
        interview_status="Scheduled"
    ).all()

    output = []

    for application in applications:

        job = JobPosition.query.get(
            application.job_id
        )

        output.append({

            "id": application.id,

            "application_id": application.id,

            "job_title": job.title if job else None,

            "company_name":
                job.company.company_name
                if job and job.company
                else None,

            "interview_date":
                application.interview_date.strftime("%Y-%m-%d")
                if application.interview_date
                else None,

            "interview_time":
                application.interview_time.strftime("%H:%M")
                if application.interview_time
                else None,

            "interview_mode":
                application.interview_mode,

            "interview_location":
                application.interview_location,

            "interview_status":
                application.interview_status

        })

    return jsonify(output), 200