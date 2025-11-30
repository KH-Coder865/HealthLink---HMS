from models import Appointment, db
from services.service_errors import ServiceError

class AppointmentService:
    @staticmethod
    def get_by_id(id=None,pid=None,did=None):
        if id:
            apt = Appointment.query.filter_by(id=id).first()
            if not apt:
                raise ServiceError(f"Appointment with id {id} not found")
            return apt
        
        if pid and did:
            appts=[]
            appts = Appointment.query.filter_by(patient_id=pid, doctor_id=did).all()
            return appts
        
        if pid:
            appts = Appointment.query.filter_by(patient_id=pid).all()
            if not appts:
                raise ServiceError(f"Appointment with patient id {pid} not found")
            return appts

        if did:
            appts = Appointment.query.filter_by(doctor_id=did).all()
            if not appts:
                raise ServiceError(f"Appointment with doctor id {did} not found")
            return appts



    @staticmethod
    def get_all():
        return Appointment.query.all()

    @staticmethod
    def delete(id):
        apt = Appointment.query.filter_by(id=id).first()
        if not apt:
            raise ServiceError(f"Appointment with id {id} not found")
        db.session.delete(apt)
        db.session.commit()

    @staticmethod
    def update(data):
        """Full update of an existing appointment record."""
        apt = Appointment.query.filter_by(id=data.get("id")).first()
        if not apt:
            raise ServiceError(f"Appointment with id {data.get('id')} not found")

        allowed_keys = {"appointment_date", "appointment_time", "status"}
        for key, value in data.items():
            if key in allowed_keys and key != "id":
                setattr(apt, key, value)

        db.session.commit()
        return apt

    @staticmethod
    def partial_update(id, data):
        """Partial update (usually to change status or reschedule)."""
        apt = Appointment.query.filter_by(id=id).first()
        if not apt:
            raise ServiceError(f"Appointment with id {id} not found")

        allowed_keys = {"appointment_date", "appointment_time", "status"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(apt, key, value)

        db.session.commit()
        return apt

    @staticmethod
    def create(data):
        """Create a new appointment."""
        allowed_keys = {"doctor_id", "patient_id", "appointment_date", "appointment_time", "status"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        required = {"doctor_id", "patient_id", "appointment_date", "appointment_time"}
        missing = required - clean_data.keys()
        if missing:
            raise ServiceError(f"Missing required fields: {', '.join(missing)}")

        apt = Appointment(**clean_data)
        db.session.add(apt)
        db.session.commit()
        return apt
    
    @staticmethod
    def get_today_appointments():
        from datetime import date
        return Appointment.query.filter_by(appointment_date=date.today(), status="scheduled").all()

    @staticmethod
    def get_pat_hist(id):
        appointments = Appointment.query.filter_by(patient_id=id, status='completed').all()
        hist = []
        for appt in appointments:
            hist.append({
                "date": str(appt.appointment_date),
                "doctor": appt.doctor.user.name,
                "dept": appt.doctor.specialization_ref.name,
                "diagnosis": appt.treatment.diagnosis if appt.treatment else None,
                "prescription": appt.treatment.prescription if appt.treatment else None,
                "tests_done": appt.treatment.tests_done if appt.treatment else None,
                "notes": appt.treatment.notes if appt.treatment else None,
            })
        print(hist)
        return hist
