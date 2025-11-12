from flask import request
from flask_restful import Resource, marshal, fields
from services import DocService
from flask_security import auth_required, roles_accepted, roles_required

doctor_fields = {
    "id": fields.Integer,
    "u_id": fields.Integer,
    "specialization_id": fields.Integer,
    "availability": fields.Raw,  # JSON
    "contact_number": fields.String,
}

@auth_required('token')
class DoctorResource(Resource):
    @roles_accepted('doctor', 'admin')
    def get(self, id):
        doc = DocService.get_by_id(id)
        return marshal(doc, doctor_fields), 200

    @roles_accepted('doctor', 'admin')
    def put(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.update(data)
        return marshal(doc, doctor_fields), 200

    @roles_accepted('doctor', 'admin')
    def patch(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.partial_update(id, data)
        return marshal(doc, doctor_fields), 200

    @roles_required('admin')
    def delete(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        DocService.delete(id)
        return {"message": "Doctor deleted successfully"}, 200


class DoctorListResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor', 'admin','patient')
    def get(self):
        docs = DocService.get_all()
        return marshal(docs, doctor_fields), 200

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        doc = DocService.create(data)
        return marshal(doc, doctor_fields), 201
