import uuid
from models import Doctor, db
from services.service_errors import ServiceError
from sqlalchemy.orm import joinedload
from extentions import cache

class DocService:
    @staticmethod
    @cache.cached(key_prefix="doctors_list", timeout=120)
    def get_all():
        return Doctor.query.options(
            joinedload(Doctor.user),
            joinedload(Doctor.specialization_ref)
        ).all()

    @staticmethod
    @cache.memoize(timeout=60)
    def get_by_id(id=None, uid=None):
        query = Doctor.query.options(
            joinedload(Doctor.user),
            joinedload(Doctor.specialization_ref)
        )
        if id:
            doc = query.filter_by(id=id).first()
            if not doc:
                raise ServiceError(f"Doctor with id {id} not found")
        elif uid:
            doc = query.filter_by(u_id=uid).first()
            if not doc:
                raise ServiceError(f"Doctor with user id {uid} not found")
        else:
            raise ServiceError("Either id or uid must be provided")
        return doc

    @staticmethod
    def delete(id):
        doc = Doctor.query.filter_by(id=id).first()
        if not doc:
            raise ServiceError(f"Doctor with id {id} not found")
        db.session.delete(doc)
        db.session.commit()
        # Invalidate caches
        cache.delete_memoized(DocService.get_by_id, id)
        cache.delete("doctors_list")

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
        # Invalidate caches
        cache.delete_memoized(DocService.get_by_id, id)
        cache.delete("doctors_list")
        return doc

    @classmethod
    def create(cls, data):
        allowed_keys = {"u_id", "specialization_id", "availability", "contact_number"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        if not clean_data.get("u_id") or not clean_data.get("specialization_id"):
            raise ServiceError("Missing required fields: 'u_id' and 'specialization_id'")

        doc = Doctor(**clean_data)
        db.session.add(doc)
        db.session.commit()
        # Invalidate full list cache
        cache.delete("doctors_list")
        return cls.get_by_id(doc.id)
