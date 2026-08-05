from flask import Blueprint, request, jsonify
from extensions import cache

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.company import Company
from models.job import JobPosition
from models.application import Application


from datetime import datetime

job_bp = Blueprint("job", __name__)


@job_bp.route("/create", methods=["POST"])
@jwt_required()
def create_job():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return jsonify({
            "message": "Company profile not found"
        }), 404

    if company.approval_status != "approved":
        return jsonify({
            "message": "Company not approved by admin"
        }), 403
    
    if company.status == "blacklisted":
        return jsonify({
            "message": "Blacklisted companies cannot create placement drives"
        }), 403

    data = request.get_json()

    # Validate required eligibility fields
    required_fields = ["title", "eligible_branch", "min_cgpa", "eligible_graduation_year", "application_deadline"]
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == "":
            return jsonify({"message": f"Missing required field: {field}"}), 400

    deadline = None
    if data.get("application_deadline"):
        try:
            deadline = datetime.strptime(data["application_deadline"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date format for application_deadline. Use YYYY-MM-DD"}), 400

    job = JobPosition(
        company_id=company.id,
        title=data["title"],
        description=data.get("description"),
        salary=data.get("salary"),
        skills_required=data.get("skills_required"),
        eligible_branch=data.get("eligible_branch"),
        min_cgpa=float(data["min_cgpa"]) if data.get("min_cgpa") is not None else None,
        eligible_graduation_year=int(data["eligible_graduation_year"]) if data.get("eligible_graduation_year") is not None else None,
        application_deadline=deadline
    )

    db.session.add(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Job created successfully"
    }), 201


@job_bp.route("/all", methods=["GET"])
@cache.cached(timeout=300)
def get_all_jobs():

    jobs = JobPosition.query.filter_by(
        status="approved"
    ).all()

    output = []

    for job in jobs:

        output.append({
            "id": job.id,
            "company_id": job.company_id,
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


@job_bp.route("/my-jobs", methods=["GET"])
@jwt_required()
def get_my_jobs():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return jsonify({
            "message": "Company profile not found"
        }), 404

    jobs = JobPosition.query.filter_by(
        company_id=company.id
    ).all()

    output = []

    for job in jobs:

        output.append({
            "id": job.id,
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

@job_bp.route("/<int:job_id>/applications", methods=["GET"])
@jwt_required()
def get_job_applications(job_id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return jsonify({
            "message": "Company profile not found"
        }), 404

    job = JobPosition.query.filter_by(
        id=job_id,
        company_id=company.id
    ).first()

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    applications = Application.query.filter_by(
        job_id=job_id
    ).all()

    output = []

    for application in applications:

        output.append({
            "application_id": application.id,
            "student_id": application.student.id,
            "student_name": application.student.full_name,
            "education": application.student.education,
            "skills": application.student.skills,
            "resume_link": application.student.resume_link,
            "branch": application.student.branch,
            "cgpa": application.student.cgpa,
            "graduation_year": application.student.graduation_year,
            "status": application.status
        })

    return jsonify(output), 200
