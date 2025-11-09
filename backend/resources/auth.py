"/login"
"/register"

from flask import Blueprint,request,jsonify
from flask_login import current_user
from flask_security.utils import verify_password, hash_password, login_user
from models import User, db
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
        "token": user.get_auth_token()
        }), 200

@auth_bp.route("/register",methods=['POST'])
def register():
    data = request.get_json()

    email = data["email"]
    password = data["password"]
    name = data["name"]
    role = data.get("role", "patient")

    active = True

    if(not email or not password or not name or not role in ["admin","doctor","patient"]):
        return jsonify({"message": "invalid input"}), 400
    
    if role=="doctor":
        active=False

    datastore=app.datastore

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "user already exists"}), 400

    datastore.create_user(email=email, name=name, password=hash_password(password), active=active)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error"}), 400


    role=datastore.find_role(role)
    user=datastore.find_user(email=email)
    datastore.add_role_to_user(user, role)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error"}), 400

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "token": user.get_auth_token()
    }), 201