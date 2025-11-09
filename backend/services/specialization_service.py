from models import Specialization, db
from services.service_errors import ServiceError

class SpecializationService:
    @staticmethod
    def get_by_id(id):
        spec = Specialization.query.filter_by(id=id).first()
        if not spec:
            raise ServiceError(f"Specialization with id {id} not found")
        return spec

    @staticmethod
    def get_all():
        return Specialization.query.all()

    @staticmethod
    def delete(id):
        spec = Specialization.query.filter_by(id=id).first()
        if not spec:
            raise ServiceError(f"Specialization with id {id} not found")
        db.session.delete(spec)
        db.session.commit()

    @staticmethod
    def partial_update(id, data):
        """Update specialization name or description."""
        spec = Specialization.query.filter_by(id=id).first()
        if not spec:
            raise ServiceError(f"Specialization with id {id} not found")

        allowed_keys = {"name", "description"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(spec, key, value)

        db.session.commit()
        return spec

    @staticmethod
    def create(data):
        """Create a new specialization."""
        allowed_keys = {"name", "description"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        if "name" not in clean_data:
            raise ServiceError("Missing required field: 'name'")

        spec = Specialization(**clean_data)
        db.session.add(spec)
        db.session.commit()
        return spec
