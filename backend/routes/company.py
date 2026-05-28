from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from extensions import db

from models.company import Company


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
        website=data.get("website")
    )

    db.session.add(company)
    db.session.commit()

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
        "approval_status": company.approval_status
    }), 200