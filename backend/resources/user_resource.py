from flask import request, jsonify
from flask_restful import Resource, marshal, fields
from services import UserService
from flask_security import auth_required, roles_required

doctor_fields = {
    "id": fields.Integer,
    "specialization_id": fields.Integer,
    "availability": fields.Raw,  # JSON field
    "contact_number": fields.String,
}

patient_fields = {
    "id": fields.Integer,
    "age": fields.Integer,
    "gender": fields.String,
    "contact_number": fields.String,
    "address": fields.String,
    "emergency_contact": fields.String,
}

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "active": fields.Boolean,
    "doctor_profile": fields.Nested(doctor_fields, allow_null=True),
    "patient_profile": fields.Nested(patient_fields, allow_null=True),
}

"""/api/user/:id"""

class UserResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self,id):
        user= UserService.get_by_id(id)
        return marshal(user, user_fields), 200
    
    @auth_required('token')
    @roles_required('admin')
    def put(self,id):
        user=UserService.get_by_id(id)
        if not user:
            return {"message":"User not found"},404
        data=request.get_json()
        UserService.update(data)
        return marshal(user, user_fields), 200
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self,id):
        user=UserService.get_by_id(id)
        if not user:
            return {"message":"User not found"},404
        UserService.delete(id)
        return marshal(user, user_fields), 200
    
    @auth_required('token')
    @roles_required('admin')
    def patch(self,id):
        user=UserService.get_by_id(id)
        if not user:
            return {"message":"User not found"},404
        data=request.get_json()
        UserService.partial_update(id,data)
        return marshal(user, user_fields), 200

"""/api/user -> get, post"""
class UserListResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        users=UserService.get_all()
        return marshal(users, user_fields), 200