"/login"
"/register"

from flask import Blueprint,request,jsonify
from flask_login import current_user
from flask_security.utils import verify_password, hash_password, login_user
from models import User, db
from services.patient_service import PatientService
from services.doctor_service import DocService

from flask import current_app as app


auth_bp=Blueprint("auth",__name__,url_prefix="/api/auth")

@auth_bp.route("/login",methods=['POST'])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    if(not email or not password):
        return jsonify({"message": "invalid input"}), 400
    user=User.query.filter_by(email=email).first_or_404()
    
    if not verify_password(password, user.password):
        return jsonify({
            "message": "invalid credentials"
        }), 401
    login_user(user)
    print(current_user)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": list(user.roles)[0].name,
        "active": user.active,
        "token": user.get_auth_token()
        }), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role")

    print(role,email,password,name,sep='\n')

    if not email or not password or not name or role not in ["doctor", "patient"]:
        return jsonify({"message": "invalid input"}), 400

    if role == "admin":
        return jsonify({"message": "admin cannot be registered"}), 400


    if User.query.filter_by(email=email).first():
        return jsonify({"message": "user already exists"}), 400

    datastore = app.datastore
    active = True if role == "patient" else False

    try:
        user = datastore.create_user(
            email=email,
            name=name,
            password=hash_password(password),
            active=active
        )
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error creating user"}), 500

    try:
        role_obj = datastore.find_role(role)
        datastore.add_role_to_user(user, role_obj)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error assigning role"}), 500

    try:
        if role == "patient":
            PatientService.create({
                "u_id": user.id,
                "gender": data.get("gender"),
                "age": data.get("age"),
                "contact_number": data.get("contact_number"),
                "emergency_contact": data.get("emergency_contact"),
                "address": data.get("address")
            })
    except:
        db.session.rollback()
        return jsonify({"message": "error creating patient profile"}), 500

    token = user.get_auth_token()

    if role=='doctor':
        return jsonify({
        "id": user.id,
        "active": user.active
    }), 201

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.roles[0].name,
        "active": user.active,
        "token": token
    }), 201
