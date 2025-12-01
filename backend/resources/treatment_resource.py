from flask import request
from flask_restful import Resource, marshal, fields
from services import TreatmentService
from flask_security import auth_required, roles_accepted, roles_required

treatment_fields = {
    "appointment_id": fields.Integer,
    "diagnosis": fields.String,
    "prescription": fields.Raw,
    "notes": fields.String,
}

class TreatmentResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor','patient','admin')
    def get(self, appointment_id):
        try:
            treat = TreatmentService.get_by_id(appointment_id)
        except Exception as e:
            return {"message": str(e)}, 404
        return marshal(treat, treatment_fields), 200

    @auth_required('token')
    @roles_required('doctor')
    def patch(self, appointment_id):
        treat = TreatmentService.get_by_id(appointment_id)
        if not treat:
            return {"message": "Treatment not found"}, 404
        data = request.get_json()
        TreatmentService.partial_update(appointment_id, data)
        return marshal(treat, treatment_fields), 200

    @auth_required('token')
    @roles_required('doctor')
    def delete(self, appointment_id):
        treat = TreatmentService.get_by_id(appointment_id)
        if not treat:
            return {"message": "Treatment not found"}, 404
        TreatmentService.delete(appointment_id)
        return {"message": "Treatment deleted successfully"}, 200

class TreatmentListResource(Resource):
    @auth_required('token')
    @roles_accepted('admin','doctor','patient')
    def get(self):
        treats = TreatmentService.get_all()
        return marshal(treats, treatment_fields), 200

    @auth_required('token')
    @roles_accepted('doctor')
    def post(self):
        data = request.get_json()
        treat = TreatmentService.create(data)
        return marshal(treat, treatment_fields), 201
