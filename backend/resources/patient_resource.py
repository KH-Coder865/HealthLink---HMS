from flask import request
from flask_restful import Resource, marshal, fields
from services import PatientService
from flask_security import auth_required, roles_accepted, roles_required

patient_fields = {
    "id": fields.Integer,
    "u_id": fields.Integer,
    "age": fields.Integer,
    "gender": fields.String,
    "contact_number": fields.String,
    "address": fields.String,
    "emergency_contact": fields.String,
}

@auth_required('token')
class PatientResource(Resource):
    @roles_accepted('patient', 'admin','doctor')
    def get(self, id):
        patient = PatientService.get_by_id(id)
        return marshal(patient, patient_fields), 200

    @roles_accepted('patient', 'admin')
    def put(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        data = request.get_json()
        PatientService.update(id, data)
        return marshal(patient, patient_fields), 200

    @roles_accepted('patient', 'admin')
    def patch(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        data = request.get_json()
        PatientService.partial_update(id, data)
        return marshal(patient, patient_fields), 200

    @roles_required('admin')
    def delete(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        PatientService.delete(id)
        return {"message": "Patient deleted successfully"}, 200

@auth_required('token')
class PatientListResource(Resource):
    @roles_accepted('doctor','patient','admin')
    def get(self):
        patients = PatientService.get_all()
        return marshal(patients, patient_fields), 200

    @roles_accepted('patient')
    def post(self):
        data = request.get_json()
        patient = PatientService.create(data)
        return marshal(patient, patient_fields), 201
