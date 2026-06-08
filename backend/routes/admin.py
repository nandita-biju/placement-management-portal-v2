from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

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
            "location": company.location
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