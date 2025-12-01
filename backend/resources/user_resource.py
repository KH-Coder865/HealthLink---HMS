from flask import request
from flask_restful import Resource, marshal, fields
from services import UserService
from flask_security import auth_required, roles_required, roles_accepted

doctor_fields = {
    "id": fields.Integer,
    "specialization_id": fields.Integer,
    "availability": fields.Raw,
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


class UserResource(Resource):

    # GET /api/user/<id>
    @auth_required('token')
    @roles_required('admin')
    def get(self, id):
        user = UserService.get_by_id(id)
        return marshal(user, user_fields), 200

    # PUT /api/user/<id>
    @auth_required('token')
    @roles_required('admin')
    def put(self, id):
        user = UserService.get_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        UserService.update(data)  # Note: data must include 'id'

        updated = UserService.get_by_id(id)
        return marshal(updated, user_fields), 200

    # DELETE /api/user/<id>
    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        user = UserService.get_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        UserService.delete(id)
        return {"message": "User deleted successfully"}, 200

    # PATCH /api/user/<id>
    @auth_required('token')
    @roles_accepted('admin', 'patient')
    def patch(self, id):
        user = UserService.get_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        UserService.partial_update(id, data)

        updated = UserService.get_by_id(id)
        return marshal(updated, user_fields), 200


class UserListResource(Resource):

    # GET /api/user
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        users = UserService.get_all()
        return marshal(users, user_fields), 200

    # POST /api/user
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        user = UserService.create(data)
        return marshal(user, user_fields), 201
