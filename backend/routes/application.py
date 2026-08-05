from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)
import csv
import io

from flask import send_file

from extensions import db

from models.student import Student
from models.company import Company
from models.job import JobPosition
from models.application import Application

from celery.result import AsyncResult
from flask import current_app

from datetime import datetime, date


application_bp = Blueprint(
    "application",
    __name__
)


@application_bp.route("/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):

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

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    if job.status != "approved":
        return jsonify({
            "message": "This placement drive is not available"
        }), 403

    # 1. Branch Validation
    if job.eligible_branch and job.eligible_branch.strip().lower() not in ["all", "all branches"]:
        student_branch = (student.branch or "").strip().lower()
        if student_branch != job.eligible_branch.strip().lower():
            return jsonify({
                "message": f"You are not eligible for this drive. Required branch: {job.eligible_branch}."
            }), 400

    # 2. CGPA Validation
    if job.min_cgpa is not None:
        if student.cgpa is None or float(student.cgpa) < float(job.min_cgpa):
            min_cgpa_str = f"{job.min_cgpa:.1f}" if isinstance(job.min_cgpa, float) and job.min_cgpa % 1 != 0 else f"{job.min_cgpa}"
            return jsonify({
                "message": f"Minimum CGPA required is {min_cgpa_str}."
            }), 400

    # 3. Graduation Year Validation
    if job.eligible_graduation_year is not None:
        if student.graduation_year is None or int(student.graduation_year) != int(job.eligible_graduation_year):
            return jsonify({
                "message": f"This drive is only for the {job.eligible_graduation_year} graduating batch."
            }), 400

    # 4. Application Deadline Validation
    if job.application_deadline:
        current_date = date.today()
        if current_date > job.application_deadline:
            return jsonify({
                "message": "The application deadline has passed."
            }), 400

    # 5. Duplicate Application Validation
    existing_application = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if existing_application:
        return jsonify({
            "message": "Already applied"
        }), 400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully"
    }), 201



@application_bp.route("/my-applications", methods=["GET"])
@jwt_required()
def get_my_applications():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403
    
    

    user_id = int(get_jwt_identity())

    from models.student import Student

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    output = []

    for application in applications:

        output.append({
            "application_id": application.id,
            "company_name": application.job.company.company_name,
            "job_title": application.job.title,
            "status": application.status,
            "applied_at": application.applied_at
        })

    return jsonify(output), 200


@application_bp.route("/<int:application_id>/status", methods=["PATCH"])
@jwt_required()
def update_application_status(application_id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company profile not found"}), 404

    if company.status == "blacklisted":
        return jsonify({
            "message": "Blacklisted companies cannot update application status"
        }), 403

    if application.job.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    allowed_statuses = [
        "Applied",
        "Shortlisted",
        "Selected",
        "Rejected"
    ]

    if data["status"] not in allowed_statuses:
        return jsonify({
            "message": "Invalid application status"
        }), 400

    application.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Application status updated successfully"
    }), 200

from tasks.export_tasks import export_student_applications

@application_bp.route("/export", methods=["GET"])
@jwt_required()
def export_applications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    task = export_student_applications.delay(student.id)

    return jsonify({
        "message": "Export started",
        "task_id": task.id
    }), 202

@application_bp.route("/export/status/<task_id>", methods=["GET"])
def export_status(task_id):

    task = AsyncResult(task_id, app=current_app.extensions["celery"])

    if task.state == "PENDING":
        return jsonify({"status": "Pending"})

    elif task.state == "SUCCESS":
        return jsonify({
            "status": "Completed",
            "filename": task.result
        })

    elif task.state == "FAILURE":
        return jsonify({"status": "Failed"})

    return jsonify({"status": task.state})