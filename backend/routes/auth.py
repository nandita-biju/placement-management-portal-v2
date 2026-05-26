from flask import Blueprint, request, jsonify

from models.user import User
from extensions import db, bcrypt

from flask_jwt_extended import create_access_token


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

    access_token = create_access_token(
        identity={
            "id": user.id,
            "role": user.role
        }
    )

    return jsonify({
        "token": access_token,
        "role": user.role
    }), 200