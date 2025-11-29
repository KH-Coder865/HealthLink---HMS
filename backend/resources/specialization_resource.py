from flask import request
from flask_restful import Resource, marshal, fields
from services import SpecializationService
from flask_security import auth_required, roles_accepted


doctor_fields = {
    "id": fields.Integer,
    "details": {
        "name": fields.String(attribute="user.name"),
        "id":fields.Integer(attribute="user.id")
    },
    "contact": fields.String(attribute="contact_number"),
    "availability": fields.Raw
}

specialization_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "doctors": fields.List(fields.Nested(doctor_fields)),
}

class SpecializationResource(Resource):
    @auth_required('token')
    @roles_accepted('patient','admin','doctor')
    def get(self):
        spec_id=request.args.get("id", type=int)
        name=request.args.get("name", type=str)

        if spec_id:
            spec = SpecializationService.get_by_id(spec_id)
        elif name:
            spec = SpecializationService.get_by_name(name)
        else:
            return {"message":"id or name required"}, 400
        
        if not spec:
            return {"message": "not found"}
        
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
    @roles_accepted('admin','patient')
    def get(self):
        specs = SpecializationService.get_all()
        return marshal(specs, specialization_fields), 200
    
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        data = request.get_json()
        spec = SpecializationService.create(data)
        return marshal(spec, specialization_fields), 201
