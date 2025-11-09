# resources/dashboard.py
from flask import Blueprint, jsonify
from flask_security import auth_required, roles_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

@dashboard_bp.route("/admin", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def admin_dashboard():
    return jsonify({
        "message": f"Welcome, Admin {current_user.name}",
        "role": "admin"
    }), 200

@dashboard_bp.route("/doctor", methods=["GET"])
@auth_required("token")
@roles_required("doctor")
def doctor_dashboard():
    return jsonify({
        "message": f"Welcome, Dr. {current_user.name}",
        "role": "doctor"
    }), 200

@dashboard_bp.route("/patient", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def patient_dashboard():
    return jsonify({
        "message": f"Welcome, {current_user.name}",
        "role": "patient"
    }), 200