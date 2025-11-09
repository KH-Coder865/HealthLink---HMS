from models import Treatment, db
from services.service_errors import ServiceError

class TreatmentService:
    @staticmethod
    def get_by_id(appointment_id):
        treat = Treatment.query.filter_by(appointment_id=appointment_id).first()
        if not treat:
            raise ServiceError(f"Treatment with appointment_id {appointment_id} not found")
        return treat

    @staticmethod
    def get_all():
        return Treatment.query.all()

    @staticmethod
    def delete(appointment_id):
        treat = Treatment.query.filter_by(appointment_id=appointment_id).first()
        if not treat:
            raise ServiceError(f"Treatment with appointment_id {appointment_id} not found")
        db.session.delete(treat)
        db.session.commit()

    @staticmethod
    def partial_update(appointment_id, data):
        """Update only the diagnosis, prescription, or notes."""
        treat = Treatment.query.filter_by(appointment_id=appointment_id).first()
        if not treat:
            raise ServiceError(f"Treatment with appointment_id {appointment_id} not found")

        allowed_keys = {"diagnosis", "prescription", "notes"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(treat, key, value)

        db.session.commit()
        return treat

    @staticmethod
    def create(data):
        """Create a new treatment record for an appointment."""
        allowed_keys = {"appointment_id", "diagnosis", "prescription", "notes"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        if "appointment_id" not in clean_data:
            raise ServiceError("Missing required field: 'appointment_id'")

        treat = Treatment(**clean_data)
        db.session.add(treat)
        db.session.commit()
        return treat
