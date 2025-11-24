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
    def delete(id):
        doc = Doctor.query.filter_by(id=id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {id} not found")
        db.session.delete(doc)
        db.session.commit()

    @staticmethod
    def update(id, data, full_update=False):
        doc = Doctor.query.filter_by(id=id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {id} not found")
        
        allowed_keys = {"specialization_id", "availability", "contact_number"}

        if full_update:  # PUT behavior
            missing = [k for k in allowed_keys if k not in data]
            if missing:
                raise ServiceError(f"Missing required fields for full update: {missing}")

        for key, value in data.items():
            if key in allowed_keys:
                setattr(doc, key, value)
            elif key in {"name", "email", "password", "active"}:
                if doc.user:
                    setattr(doc.user, key, value)
                else:
                    raise ServiceError(f"Doctor {id} has no associated user to update {key}")

        db.session.commit()
        return doc



    @staticmethod
    def create(data):
        allowed_keys = {"u_id", "specialization_id", "availability", "contact_number"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}
        print("CLEAN DATA", data)
        # Validate required keys
        if not clean_data.get("u_id") or not clean_data.get("specialization_id"):
            raise ServiceError("Missing required fields: 'u_id' and 'specialization_id'")

        doc = Doctor(**clean_data)
        db.session.add(doc)
        db.session.commit()