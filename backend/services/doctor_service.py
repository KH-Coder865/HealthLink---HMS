import uuid
from models import Doctor, db
from services.service_errors import ServiceError

class DocService:
    @staticmethod
    def get_by_id(id):
        doc = Doctor.query.filter_by(id=id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {id} not found")
        return doc

    @staticmethod
    def get_all():
        return Doctor.query.all()

    @staticmethod
    def delete(u_id):
        doc = Doctor.query.filter_by(u_id=u_id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {u_id} not found")
        db.session.delete(doc)
        db.session.commit()

    @staticmethod
    def update(data):
        """{'u_id':1,'name':'new name',...}"""
        print(data["u_id"])
        doc = Doctor.query.filter_by(u_id=data.get("u_id")).first()
        if not doc:
            raise ServiceError(f"Doctor with id {data.get('u_id')} not found")
        
        allowed_keys = {"u_id", "specialization_id", "availability", "contact_number"}

    
        for key, value in data.items():
            if key in allowed_keys and key != "u_id":
                setattr(doc, key, value)
        
        db.session.commit()

    @staticmethod
    def partial_update(id, data):
        doc = Doctor.query.filter_by(id=id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {id} not found")
        
        allowed_keys = {"specialization_id", "availability", "contact_number"}

    
        for key, value in data.items():
            if key in allowed_keys:
                setattr(doc, key, value)
            elif key == "patient_profile":
                patient_profile_data = value
                if not hasattr(doc, "patient_profile") or not doc.patient_profile:
                    raise ServiceError(f"Doctor {id} has no patient profile")

                for subkey, subval in patient_profile_data.items():
                    setattr(doc.patient_profile, subkey, subval)
            elif key == "doctor_profile":
                doctor_profile_data = value
                if not hasattr(doc, "doctor_profile") or not doc.doctor_profile:
                    raise ServiceError(f"Doctor {id} has no doctor profile")

                for subkey, subval in doctor_profile_data.items():
                    setattr(doc.doctor_profile, subkey, subval)
        
        db.session.commit()

    @staticmethod
    def create(data):
        allowed_keys = {"u_id", "specialization_id", "availability", "contact_number"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        # Validate required keys
        if not clean_data.get("u_id") or not clean_data.get("specialization_id"):
            raise ServiceError("Missing required fields: 'u_id' and 'specialization_id'")

        doc = Doctor(**clean_data)
        db.session.add(doc)
        db.session.commit()