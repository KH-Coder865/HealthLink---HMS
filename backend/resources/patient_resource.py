from flask import request
from flask_restful import Resource, marshal, fields
from services import PatientService
from flask_security import auth_required, roles_accepted, roles_required

credentials = {
    "id": fields.Integer(attribute=lambda pat: pat.user.id if pat.user else 0),
    "name": fields.String(attribute=lambda pat: pat.user.name if pat.user else "Unknown"),
    "email": fields.String(attribute=lambda pat: pat.user.email if pat.user else ""),
    "active": fields.Boolean(attribute=lambda pat: pat.user.active if pat.user else False),
}

patient_fields = {
    "id": fields.Integer,
    "details": fields.Nested(credentials, attribute=lambda pat: pat),
    "age": fields.Integer(attribute=lambda pat: pat.age if pat else None),
    "gender": fields.String(attribute=lambda pat: pat.gender if pat else ""),
    "contact_number": fields.String(attribute=lambda pat: pat.contact_number if pat else ""),
    "address": fields.String(attribute=lambda pat: pat.address if pat else ""),
    "emergency_contact": fields.String(attribute=lambda pat: pat.emergency_contact if pat else ""),
    "created_at": fields.DateTime(attribute=lambda pat: pat.created_at if pat else None),
    "updated_at": fields.DateTime(attribute=lambda pat: pat.updated_at if pat else None),
}


class PatientResource(Resource):
    @auth_required('token')
    @roles_accepted('patient', 'admin','doctor')
    def get(self, id):
        patient = PatientService.get_by_id(id)
        return marshal(patient, patient_fields), 200

    @auth_required('token')
    @roles_accepted('patient', 'admin')
    def put(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        data = request.get_json()
        PatientService.update(id, data)
        return marshal(patient, patient_fields), 200

    @auth_required('token')
    @roles_accepted('patient', 'admin')
    def patch(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        data = request.get_json()
        PatientService.partial_update(id, data)
        return marshal(patient, patient_fields), 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        PatientService.delete(id)
        return {"message": "Patient deleted successfully"}, 200


class PatientListResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor','patient','admin')
    def get(self):
        patients = PatientService.get_all()
        return marshal(patients, patient_fields), 200

    @auth_required('token')
    @roles_accepted('patient')
    def post(self):
        data = request.get_json()
        patient = PatientService.create(data)
        return marshal(patient, patient_fields), 201
