from flask import request
from flask_restful import Resource, marshal, fields
from services import TreatmentService

treatment_fields = {
    "appointment_id": fields.Integer,
    "diagnosis": fields.String,
    "prescription": fields.Raw,
    "notes": fields.String,
}

class TreatmentResource(Resource):
    def get(self, appointment_id):
        treat = TreatmentService.get_by_id(appointment_id)
        return marshal(treat, treatment_fields), 200

    def patch(self, appointment_id):
        treat = TreatmentService.get_by_id(appointment_id)
        if not treat:
            return {"message": "Treatment not found"}, 404
        data = request.get_json()
        TreatmentService.partial_update(appointment_id, data)
        return marshal(treat, treatment_fields), 200

    def delete(self, appointment_id):
        treat = TreatmentService.get_by_id(appointment_id)
        if not treat:
            return {"message": "Treatment not found"}, 404
        TreatmentService.delete(appointment_id)
        return {"message": "Treatment deleted successfully"}, 200


class TreatmentListResource(Resource):
    def get(self):
        treats = TreatmentService.get_all()
        return marshal(treats, treatment_fields), 200

    def post(self):
        data = request.get_json()
        treat = TreatmentService.create(data)
        return marshal(treat, treatment_fields), 201
