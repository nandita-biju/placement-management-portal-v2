from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_dashboard():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Welcome Admin Dashboard"
    })


@dashboard_bp.route("/student", methods=["GET"])
@jwt_required()
def student_dashboard():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Welcome Student Dashboard"
    })


@dashboard_bp.route("/company", methods=["GET"])
@jwt_required()
def company_dashboard():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Welcome Company Dashboard"
    })