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
            "approval_status": company.approval_status
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
            "skills": student.skills
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

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully"
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
