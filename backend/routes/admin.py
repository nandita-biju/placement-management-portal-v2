from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from extensions import db

from models.student import Student
from models.company import Company
from models.job import JobPosition
from models.application import Application

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    return jsonify({
        "students": Student.query.count(),
        "companies": Company.query.count(),
        "jobs": JobPosition.query.count(),
        "applications": Application.query.count()
    }), 200

@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def get_companies():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    companies = Company.query.all()

    output = []

    for company in companies:

        output.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status,
            "status": company.status
        })

    return jsonify(output), 200

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    students = Student.query.all()

    output = []

    for student in students:

        output.append({
            "id": student.id,
            "full_name": student.full_name,
            "education": student.education,
            "skills": student.skills,
            "is_active": student.is_active
        })

    return jsonify(output), 200

@admin_bp.route("/company/<int:company_id>/approve", methods=["PATCH"])
@jwt_required()
def approve_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval_status = "approved"
    company.status = "active"

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully"
    }), 200

@admin_bp.route("/company/<int:company_id>/reject", methods=["PATCH"])
@jwt_required()
def reject_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval_status = "rejected"
    company.status = "inactive"

    db.session.commit()

    return jsonify({
        "message": "Company rejected"
    }), 200

@admin_bp.route("/students/search", methods=["GET"])
@jwt_required()
def search_students():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    skill = request.args.get("skill")

    students = Student.query.filter(
        Student.skills.ilike(f"%{skill}%")
    ).all()

    output = []

    for student in students:
        output.append({
            "id": student.id,
            "full_name": student.full_name,
            "skills": student.skills,
            "education": student.education
        })

    return jsonify(output), 200

@admin_bp.route("/companies/search", methods=["GET"])
@jwt_required()
def search_companies():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    industry = request.args.get("industry")

    companies = Company.query.filter(
        Company.industry.ilike(f"%{industry}%")
    ).all()

    output = []

    for company in companies:
        output.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location
        })

    return jsonify(output), 200

@admin_bp.route("/approve-drive/<int:job_id>", methods=["PUT"])
@jwt_required()
def approve_drive(job_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Drive not found"}), 404

    job.status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Drive approved successfully"
    }), 200

@admin_bp.route("/reject-drive/<int:job_id>", methods=["PUT"])
@jwt_required()
def reject_drive(job_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Drive not found"}), 404

    job.status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Drive rejected successfully"
    }), 200

@admin_bp.route("/drives", methods=["GET"])
@jwt_required()
def get_all_drives():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    jobs = JobPosition.query.all()

    output = []

    for job in jobs:
        output.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "skills_required": job.skills_required,
            "status": job.status,
            "company_id": job.company_id
        })

    return jsonify(output), 200

@admin_bp.route(
    "/student/<int:student_id>/deactivate",
    methods=["PUT"]
)
@jwt_required()
def deactivate_student(student_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    student.is_active = False

    db.session.commit()

    return jsonify({
        "message": "Student deactivated"
    }), 200


@admin_bp.route(
    "/student/<int:student_id>/activate",
    methods=["PUT"]
)
@jwt_required()
def activate_student(student_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    student.is_active = True

    db.session.commit()

    return jsonify({
        "message": "Student activated successfully"
    }), 200


@admin_bp.route(
    "/company/<int:company_id>/deactivate",
    methods=["PUT"]
)
@jwt_required()
def deactivate_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.status = "deactivated"

    db.session.commit()

    return jsonify({
        "message": "Company deactivated"
    }), 200



@admin_bp.route(
    "/company/<int:company_id>/activate",
    methods=["PUT"]
)
@jwt_required()
def activate_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.status = "active"

    db.session.commit()

    return jsonify({
        "message": "Company activated"
    }), 200



@admin_bp.route(
    "/company/<int:company_id>/blacklist",
    methods=["PUT"]
)
@jwt_required()
def blacklist_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.status = "blacklisted"

    db.session.commit()

    return jsonify({
        "message": "Company blacklisted"
    }), 200



@admin_bp.route(
    "/company/<int:company_id>/unblacklist",
    methods=["PUT"]
)
@jwt_required()
def unblacklist_company(company_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.status = "active"

    db.session.commit()

    return jsonify({
        "message": "Company unblacklisted"
    }), 200