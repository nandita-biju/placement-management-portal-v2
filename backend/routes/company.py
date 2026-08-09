from flask import Blueprint, request, jsonify
from extensions import cache
from sqlalchemy import func
from datetime import datetime
from models.application import Application

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.company import Company
from models.job import JobPosition
from models.user import User
from models.application import Application


company_bp = Blueprint("company", __name__)


@company_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_company_profile():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({
            "message": "Access denied"
        }), 403

    user_id = int(get_jwt_identity())

    existing_profile = Company.query.filter_by(
        user_id=user_id
    ).first()

    if existing_profile:
        return jsonify({
            "message": "Company profile already exists"
        }), 400
    
    

    data = request.get_json()

    company = Company(
        user_id=user_id,
        company_name=data["company_name"],
        industry=data.get("industry"),
        location=data.get("location"),
        website=data.get("website"),
        hr_contact=data.get("hr_contact")
    )

    db.session.add(company)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Company profile created successfully"
    }), 201


@company_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_company_profile():

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

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "hr_contact": company.hr_contact,
        "approval_status": company.approval_status,
        "status": company.status
    }), 200


@company_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_company_profile():

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

    data = request.get_json()

    company.company_name = data["company_name"]
    company.industry = data.get("industry")
    company.location = data.get("location")
    company.website = data.get("website")
    company.hr_contact = data.get("hr_contact")

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Company profile updated successfully"
    }), 200

@company_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_company_dashboard():
    

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

    user = User.query.get(user_id)

    drives = (
        db.session.query(
            JobPosition,
            func.count(Application.id).label("applicant_count")
        )
        .outerjoin(
            Application,
            Application.job_id == JobPosition.id
        )
        .filter(
            JobPosition.company_id == company.id
        )
        .group_by(
            JobPosition.id
        )
        .order_by(
            JobPosition.created_at.desc()
        )
        .all()
    )

    drive_data = []

    for job, applicant_count in drives:
        drive_data.append({
            "drive_id": job.id,
            "title": job.title,
            "location": job.location,
            "deadline": (
                job.deadline.strftime("%Y-%m-%d")
                if job.deadline
                else None
            ),
            "created_at": (
                job.created_at.strftime("%Y-%m-%d")
                if job.created_at
                else None
            ),
            "applicant_count": int(applicant_count)
        })

    return jsonify({
        "company": {
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "website": company.website,
            "hr_contact": company.hr_contact,
            "email": user.email if user else None,
            "approval_status": company.approval_status,
            "status": company.status
        },
        "total_drives": len(drive_data),
        "total_applicants": sum(
            drive["applicant_count"]
            for drive in drive_data
        ),
        "drives": drive_data
    }), 200

@company_bp.route("/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company_by_id(company_id):

    claims = get_jwt()

    if claims["role"] not in ["admin", "student"]:
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    # Students can only view approved companies
    if claims["role"] == "student":
        if company.approval_status != "approved":
            return jsonify({
                "message": "Company profile not available"
            }), 403

    return jsonify({
        "id": company.id,
        "company_name": company.company_name,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "hr_contact": company.hr_contact,
        "approval_status": company.approval_status,
        "status": company.status
    }), 200

@company_bp.route("/applications/<int:application_id>/interview", methods=["POST"])
@jwt_required()
def schedule_interview(application_id):

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

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    # Make sure this application belongs to this company
    job = JobPosition.query.get(application.job_id)

    if not job or job.company_id != company.id:
        return jsonify({
            "message": "You cannot manage this application"
        }), 403

    # Interview can only be scheduled for shortlisted students
    if application.status != "Shortlisted":
        return jsonify({
            "message": "Interview can only be scheduled for shortlisted students"
        }), 400

    data = request.get_json()

    if not data.get("interview_date"):
        return jsonify({
            "message": "Interview date is required"
        }), 400

    if not data.get("interview_time"):
        return jsonify({
            "message": "Interview time is required"
        }), 400

    if not data.get("interview_mode"):
        return jsonify({
            "message": "Interview mode is required"
        }), 400

    try:

        application.interview_date = datetime.strptime(
            data["interview_date"],
            "%Y-%m-%d"
        ).date()

        application.interview_time = datetime.strptime(
            data["interview_time"],
            "%H:%M"
        ).time()

    except ValueError:

        return jsonify({
            "message": "Invalid date or time format"
        }), 400

    application.interview_mode = data["interview_mode"]

    application.interview_location = data.get(
        "interview_location"
    )

    application.interview_status = "Scheduled"

    db.session.commit()

    return jsonify({
        "message": "Interview scheduled successfully"
    }), 200