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
            "resume_link": student.resume_link,
            "is_active": student.is_active,
            "status": student.status
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

from sqlalchemy import or_

@admin_bp.route("/students/search", methods=["GET"])
@jwt_required()
def search_students():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    query = request.args.get("query", "")

    students = Student.query.filter(
        or_(
            Student.full_name.ilike(f"%{query}%"),
            Student.skills.ilike(f"%{query}%"),
            Student.education.ilike(f"%{query}%")
        )
    ).all()

    output = []

    for student in students:

        output.append({
            "id": student.id,
            "full_name": student.full_name,
            "education": student.education,
            "skills": student.skills,
            "resume_link": student.resume_link,
            "is_active": student.is_active,
            "status": student.status
        })

    return jsonify(output), 200

from sqlalchemy import or_

@admin_bp.route("/companies/search", methods=["GET"])
@jwt_required()
def search_companies():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    query = request.args.get("query", "")

    companies = Company.query.filter(
        or_(
            Company.company_name.ilike(f"%{query}%"),
            Company.industry.ilike(f"%{query}%"),
            Company.location.ilike(f"%{query}%")
        )
    ).all()

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



@admin_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_all_applications():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    applications = Application.query.all()

    output = []

    for application in applications:

        output.append({
            "id": application.id,
            "student_name": application.student.full_name,
            "company_name": application.job.company.company_name,
            "drive_title": application.job.title,
            "status": application.status,
            "applied_at": application.applied_at.strftime("%d-%m-%Y")
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


@admin_bp.route(
    "/blacklist-student/<int:student_id>",
    methods=["PUT"]
)
@jwt_required()
def blacklist_student(student_id):

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

    student.status = "blacklisted"

    db.session.commit()

    return jsonify({
        "message": "Student blacklisted successfully"
    }), 200


@admin_bp.route(
    "/unblacklist-student/<int:student_id>",
    methods=["PUT"]
)
@jwt_required()
def unblacklist_student(student_id):

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

    student.status = "active"

    db.session.commit()

    return jsonify({
        "message": "Student unblacklisted successfully"
    }), 200


@admin_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_reports():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    # ==========================
    # BASIC COUNTS
    # ==========================

    total_students = Student.query.count()

    total_companies = Company.query.count()

    total_drives = JobPosition.query.count()

    total_applications = Application.query.count()


    # ==========================
    # APPLICATION STATISTICS
    # ==========================

    selected = Application.query.filter_by(
        status="Selected"
    ).count()

    shortlisted = Application.query.filter_by(
        status="Shortlisted"
    ).count()

    rejected = Application.query.filter_by(
        status="Rejected"
    ).count()

    applied = Application.query.filter_by(
        status="Applied"
    ).count()


    # ==========================
    # COMPANY STATISTICS
    # ==========================

    active_companies = Company.query.filter_by(
        status="active"
    ).count()

    blacklisted_companies = Company.query.filter_by(
        status="blacklisted"
    ).count()

    deactivated_companies = Company.query.filter_by(
        status="deactivated"
    ).count()

    pending_companies = Company.query.filter_by(
        approval_status="pending"
    ).count()

    approved_companies = Company.query.filter_by(
        approval_status="approved"
    ).count()

    rejected_companies = Company.query.filter_by(
        approval_status="rejected"
    ).count()


    # ==========================
    # STUDENT STATISTICS
    # ==========================

    active_students = Student.query.filter_by(
        is_active=True
    ).count()

    deactivated_students = Student.query.filter_by(
        is_active=False
    ).count()

    blacklisted_students = Student.query.filter_by(
        status="blacklisted"
    ).count()


    # ==========================
    # PLACEMENT RATE
    # ==========================

    if total_students > 0:

        placement_rate = round(
            (selected / total_students) * 100,
            2
        )

    else:

        placement_rate = 0


    # ==========================
    # DRIVE STATISTICS
    # ==========================

    drive_statistics = []

    drives = JobPosition.query.all()

    for drive in drives:

        applicants = Application.query.filter_by(
            job_id=drive.id
        ).count()

        shortlisted_count = Application.query.filter_by(
            job_id=drive.id,
            status="Shortlisted"
        ).count()

        selected_count = Application.query.filter_by(
            job_id=drive.id,
            status="Selected"
        ).count()

        rejected_count = Application.query.filter_by(
            job_id=drive.id,
            status="Rejected"
        ).count()

        drive_statistics.append({

            "drive_id": drive.id,

            "company_name":
                drive.company.company_name,

            "title":
                drive.title,

            "applicants":
                applicants,

            "shortlisted":
                shortlisted_count,

            "selected":
                selected_count,

            "rejected":
                rejected_count

        })


    # ==========================
    # FINAL RESPONSE
    # ==========================

    return jsonify({

        "students": {

            "total": total_students,

            "active": active_students,

            "blacklisted":
                blacklisted_students,

            "deactivated":
                deactivated_students

        },

        "companies": {

            "total": total_companies,

            "active":
                active_companies,

            "blacklisted":
                blacklisted_companies,

            "deactivated":
                deactivated_companies,

            "pending":
                pending_companies,

            "approved":
                approved_companies,

            "rejected":
                rejected_companies

        },

        "drives": {

            "total":
                total_drives

        },

        "applications": {

            "total":
                total_applications,

            "applied":
                applied,

            "shortlisted":
                shortlisted,

            "selected":
                selected,

            "rejected":
                rejected

        },

        "placement_rate":
            placement_rate,

        "drive_statistics":
            drive_statistics

    }), 200

@admin_bp.route(
    "/student/<int:student_id>/placement-history",
    methods=["GET"]
)
@jwt_required()
def get_student_placement_history(student_id):

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

    applications = (
        Application.query
        .filter_by(student_id=student_id)
        .order_by(Application.applied_at.desc())
        .all()
    )

    history = []

    for application in applications:
        job = JobPosition.query.get(application.job_id)

        if not job:
            continue

        company = Company.query.get(job.company_id)

        history.append({
            "application_id": application.id,
            "company_name": (
                company.company_name
                if company
                else "Company"
            ),
            "job_title": job.title,
            "status": application.status,
            "applied_at": (
                application.applied_at.isoformat()
                if application.applied_at
                else None
            ),
            "interview_status": application.interview_status,
            "interview_date": (
                application.interview_date.isoformat()
                if application.interview_date
                else None
            ),
            "interview_time": (
                application.interview_time.strftime("%H:%M")
                if application.interview_time
                else None
            ),
            "interview_mode": application.interview_mode
        })

    return jsonify({
        "student_name": student.full_name,
        "history": history
    }), 200


@admin_bp.route(
    "/company/<int:company_id>/drive-history",
    methods=["GET"]
)
@jwt_required()
def get_company_drive_history(company_id):

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

    drives = (
        JobPosition.query
        .filter_by(company_id=company_id)
        .order_by(JobPosition.id.desc())
        .all()
    )

    output = []

    for drive in drives:
        applicant_count = Application.query.filter_by(
            job_id=drive.id
        ).count()

        deadline = drive.application_deadline

        output.append({
            "drive_id": drive.id,
            "title": drive.title,
            "salary": drive.salary,
            "eligible_branch": drive.eligible_branch,
            "application_deadline": (
                deadline.isoformat()
                if hasattr(deadline, "isoformat")
                else deadline
            ),
            "status": drive.status,
            "applicant_count": applicant_count
        })

    return jsonify({
        "company_name": company.company_name,
        "drives": output
    }), 200