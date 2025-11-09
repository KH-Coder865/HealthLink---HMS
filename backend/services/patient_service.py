from models import Patient, db
from services.service_errors import ServiceError

class PatientService:
    @staticmethod
    def get_all():
        return Patient.query.all()

    @staticmethod
    def get_by_id(id):
        patient = Patient.query.get(id)
        if not patient:
            raise ServiceError(f"Patient with id {id} not found")
        return patient

    @staticmethod
    def create(data):
        """Create a new patient profile"""
        allowed_keys = {"u_id", "age", "gender", "contact_number", "address", "emergency_contact"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        if "u_id" not in clean_data:
            raise ServiceError("Missing required field: 'u_id'")

        patient = Patient(**clean_data)
        db.session.add(patient)
        db.session.commit()
        return patient

    @staticmethod
    def update(id, data):
        """Full update (replaces all fields except id)"""
        patient = Patient.query.get(id)
        if not patient:
            raise ServiceError(f"Patient with id {id} not found")

        allowed_keys = {"u_id", "age", "gender", "contact_number", "address", "emergency_contact"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(patient, key, value)

        db.session.commit()
        return patient

    @staticmethod
    def partial_update(id, data):
        """Partial update (patch specific fields)"""
        patient = Patient.query.get(id)
        if not patient:
            raise ServiceError(f"Patient with id {id} not found")

        allowed_keys = {"age", "gender", "contact_number", "address", "emergency_contact"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(patient, key, value)

        db.session.commit()
        return patient

    @staticmethod
    def delete(id):
        patient = Patient.query.get(id)
        if not patient:
            raise ServiceError(f"Patient with id {id} not found")
        db.session.delete(patient)
        db.session.commit()
        return patient
