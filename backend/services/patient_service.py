from models import Patient, db
from services.service_errors import ServiceError
from sqlalchemy.orm import joinedload
from extentions import cache

class PatientService:

    @staticmethod
    @cache.cached(key_prefix="patients_list", timeout=300)
    def get_all():
        return Patient.query.options(joinedload(Patient.user)).all()

    @staticmethod
    @cache.memoize(timeout=300)
    def get_by_id(id=None, uid=None):
        query = Patient.query.options(joinedload(Patient.user))
        if id:
            pat = query.filter_by(id=id).first()
            if not pat:
                raise ServiceError(f"Patient with id {id} not found")
        elif uid:
            pat = query.filter_by(u_id=uid).first()
            if not pat:
                raise ServiceError(f"Patient with user id {uid} not found")
        else:
            raise ServiceError("Either id or uid must be provided")
        return pat

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

        # Invalidate caches
        cache.delete("patients_list")
        cache.delete_memoized(PatientService.get_by_id, patient.id)
        cache.delete_memoized(PatientService.get_by_id, uid=patient.u_id)

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

        # Invalidate caches
        cache.delete("patients_list")
        cache.delete_memoized(PatientService.get_by_id, id)
        cache.delete_memoized(PatientService.get_by_id, uid=patient.u_id)

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

        # Invalidate caches
        cache.delete("patients_list")
        cache.delete_memoized(PatientService.get_by_id, id)
        cache.delete_memoized(PatientService.get_by_id, uid=patient.u_id)

        return patient

    @staticmethod
    def delete(id):
        patient = Patient.query.get(id)
        if not patient:
            raise ServiceError(f"Patient with id {id} not found")
        db.session.delete(patient)
        db.session.commit()

        # Invalidate caches
        cache.delete("patients_list")
        cache.delete_memoized(PatientService.get_by_id, id)
        cache.delete_memoized(PatientService.get_by_id, uid=patient.u_id)

        return patient
