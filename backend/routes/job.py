from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.company import Company
from models.job import JobPosition


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

    '''if company.approval_status != "approved":
        return jsonify({
            "message": "Company not approved by admin"
        }), 403'''

    data = request.get_json()

    job = JobPosition(
        company_id=company.id,
        title=data["title"],
        description=data.get("description"),
        salary=data.get("salary"),
        skills_required=data.get("skills_required")
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job created successfully"
    }), 201


@job_bp.route("/all", methods=["GET"])
def get_all_jobs():

    jobs = JobPosition.query.all()

    output = []

    for job in jobs:

        output.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "skills_required": job.skills_required,
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
            "status": job.status
        })

    return jsonify(output), 200