from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.student import Student
from models.company import Company
from models.job import JobPosition
from models.application import Application


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
            "job_title": application.job.title,
            "status": application.status,
            "applied_at": application.applied_at
        })

    return jsonify(output), 200