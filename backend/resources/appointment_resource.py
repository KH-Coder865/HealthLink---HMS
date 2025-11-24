from flask import request
from flask_restful import Resource, marshal, fields
from services import AppointmentService
from flask_security import auth_required, roles_accepted

treatment_fields = {
    "diagnosis": fields.String,
    "tests_done": fields.String,
    "prescription": fields.Raw,
    "notes": fields.String,
}

appointment_fields = {
    "id": fields.Integer,
    "doctor_id": fields.Integer,
    "patient_id": fields.Integer,
    "treatment": fields.Nested(treatment_fields, default=None),
    "appointment_date": fields.String,
    "appointment_time": fields.String,
    "status": fields.String,
}


class AppointmentResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor', 'admin','patient')
    def get(self):
        appt_id = request.args.get("id", type=int)
        pid = request.args.get("pid", type=int)
        did = request.args.get("did", type=int)

        if appt_id:
            appt = AppointmentService.get_by_id(id=appt_id)
            return marshal(appt, appointment_fields), 200

        if pid and did:
            appts = AppointmentService.get_by_id(pid=pid,did=did)
            return marshal(appts, appointment_fields), 200

        if pid:
            appts = AppointmentService.get_by_id(pid=pid)
            return marshal(appts, appointment_fields), 200

        if did:
            appts = AppointmentService.get_by_id(did=did)
            return marshal(appts, appointment_fields), 200

        return {"error": "Provide id or pid or did"}, 400
    
    @auth_required('token')
    @roles_accepted('doctor', 'admin')
    def patch(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        data = request.get_json()
        AppointmentService.partial_update(id, data)
        return marshal(appt, appointment_fields), 200

    @auth_required('token')
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
