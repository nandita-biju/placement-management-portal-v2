from flask import Blueprint, request, jsonify

from models.job import JobPosition
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.user import User
from models.student import Student


student_bp = Blueprint("student", __name__)


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
        experience=data.get("experience")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "Student profile created successfully"
    }), 201


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
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
        "experience": profile.experience
    }), 200

@student_bp.route("/drives", methods=["GET"])
@jwt_required()
def get_all_drives():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({
            "message": "Access denied"
        }), 403

    jobs = JobPosition.query.filter_by(status="approved").all()

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