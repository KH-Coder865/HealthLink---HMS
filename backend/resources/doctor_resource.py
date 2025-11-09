from flask import request
from flask_restful import Resource, marshal, fields
from services import DocService

doctor_fields = {
    "id": fields.Integer,
    "u_id": fields.Integer,
    "specialization_id": fields.Integer,
    "availability": fields.Raw,  # JSON
    "contact_number": fields.String,
}

class DoctorResource(Resource):
    def get(self, id):
        doc = DocService.get_by_id(id)
        return marshal(doc, doctor_fields), 200

    def put(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.update(data)
        return marshal(doc, doctor_fields), 200

    def patch(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.partial_update(id, data)
        return marshal(doc, doctor_fields), 200

    def delete(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        DocService.delete(id)
        return {"message": "Doctor deleted successfully"}, 200


class DoctorListResource(Resource):
    def get(self):
        docs = DocService.get_all()
        return marshal(docs, doctor_fields), 200

    def post(self):
        data = request.get_json()
        doc = DocService.create(data)
        return marshal(doc, doctor_fields), 201
