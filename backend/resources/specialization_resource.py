from flask import request
from flask_restful import Resource, marshal, fields
from services import SpecializationService
from flask_security import auth_required, roles_accepted, roles_required

specialization_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}

class SpecializationResource(Resource):
    @auth_required('token')
    @roles_accepted('patient','admin','doctor')
    def get(self, id):
        spec = SpecializationService.get_by_id(id)
        return marshal(spec, specialization_fields), 200

    @auth_required('token')
    @roles_accepted('admin')
    def patch(self, id):
        spec = SpecializationService.get_by_id(id)
        if not spec:
            return {"message": "Specialization not found"}, 404
        data = request.get_json()
        SpecializationService.partial_update(id, data)
        return marshal(spec, specialization_fields), 200

    @auth_required('token')
    @roles_accepted('admin')
    def delete(self, id):
        spec = SpecializationService.get_by_id(id)
        if not spec:
            return {"message": "Specialization not found"}, 404
        SpecializationService.delete(id)
        return {"message": "Specialization deleted successfully"}, 200


class SpecializationListResource(Resource):
    @auth_required('token')
    @roles_accepted('admin')
    def get(self):
        specs = SpecializationService.get_all()
        return marshal(specs, specialization_fields), 200
    
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        data = request.get_json()
        spec = SpecializationService.create(data)
        return marshal(spec, specialization_fields), 201
