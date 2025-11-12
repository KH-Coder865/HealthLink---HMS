from flask import request
from flask_restful import Resource, marshal, fields
from services import AppointmentService
from flask_security import auth_required, roles_accepted, roles_required

appointment_fields = {
    "id": fields.Integer,
    "doctor_id": fields.Integer,
    "patient_id": fields.Integer,
    "appointment_date": fields.String,
    "appointment_time": fields.String,
    "status": fields.String,
}


@auth_required('token')
class AppointmentResource(Resource):
    @roles_accepted('doctor', 'admin','patient')
    def get(self, id):
        appt = AppointmentService.get_by_id(id)
        return marshal(appt, appointment_fields), 200
    
    @roles_accepted('doctor', 'admin')
    def patch(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        data = request.get_json()
        AppointmentService.partial_update(id, data)
        return marshal(appt, appointment_fields), 200

    @roles_accepted('doctor', 'admin', 'patient')
    def delete(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        AppointmentService.delete(id)
        return {"message": "Appointment deleted successfully"}, 200


class AppointmentListResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor', 'admin', 'patient')
    def get(self):
        appts = AppointmentService.get_all()
        return marshal(appts, appointment_fields), 200

    @auth_required('token')
    @roles_accepted('admin', 'doctor', 'patient')
    def post(self):
        data = request.get_json()
        appt = AppointmentService.create(data)
        return marshal(appt, appointment_fields), 201
