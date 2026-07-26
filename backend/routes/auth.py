from flask import Blueprint, request, jsonify

from models.user import User
from extensions import db, bcrypt

from flask_jwt_extended import create_access_token

from models.company import Company

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    student = User(
        email=data["email"],
        password=hashed_password,
        role="student"
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"}), 201


@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    company = User(
        email=data["email"],
        password=hashed_password,
        role="company"
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    password_correct = bcrypt.check_password_hash(
        user.password,
        data["password"]
    )

    if not password_correct:
        return jsonify({"message": "Invalid credentials"}), 401
    
    if user.role == "company":

        company = Company.query.filter_by(
            user_id=user.id
        ).first()

        if company:

            if company.approval_status == "pending":
                return jsonify({
                    "message": "Company approval pending"
                }), 403

            if company.approval_status == "rejected":
                return jsonify({
                    "message": "Company registration rejected"
                }), 403

            if company.status == "deactivated":
                return jsonify({
                    "message": "Company account is deactivated"
                }), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "token": access_token,
        "role": user.role
    }), 200