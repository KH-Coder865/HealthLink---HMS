import uuid
from models import User, db
from services.service_errors import ServiceError
from extentions import cache

class UserService:

    @staticmethod
    @cache.memoize(timeout=300)
    def get_by_id(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ServiceError(f"User with id {id} not found")
        return user

    @staticmethod
    @cache.cached(key_prefix="users_list", timeout=300)
    def get_all():
        return User.query.all()

    @staticmethod
    def create(data):
        allowed_keys = {"name", "email", "password", "fs_uniquifier", "active"}
        clean_data = {k: v for k, v in data.items() if k in allowed_keys}

        if not clean_data.get("email") or not clean_data.get("password"):
            raise ServiceError("Missing required fields: 'email' and 'password'")

        clean_data.setdefault("fs_uniquifier", str(uuid.uuid4()))
        clean_data.setdefault("active", True)

        user = User(**clean_data)
        db.session.add(user)
        db.session.commit()

        # Invalidate caches
        cache.delete("users_list")
        cache.delete("doctors_list")
        cache.delete("patients_list")
        cache.delete_memoized(UserService.get_by_id, user.id)

        return user

    @staticmethod
    def update(data):
        user = User.query.filter_by(id=data.get("id")).first()
        if not user:
            raise ServiceError(f"User with id {data.get('id')} not found")

        allowed_keys = {"name", "email", "password", "active"}
        for key, value in data.items():
            if key in allowed_keys and key != "id":
                setattr(user, key, value)
        db.session.commit()

        # Invalidate caches
        cache.delete("users_list")
        cache.delete("doctors_list")
        cache.delete("patients_list")
        cache.delete("appointments_list")
        cache.delete_memoized(UserService.get_by_id, user.id)

        return user

    @staticmethod
    def partial_update(id, data):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ServiceError(f"User with id {id} not found")

        allowed_keys = {"name", "email", "password", "active"}
        for key, value in data.items():
            if key in allowed_keys:
                setattr(user, key, value)
            elif key == "patient_profile":
                patient_data = value
                if not user.patient_profile:
                    raise ServiceError(f"User {id} has no patient profile")
                for subkey, subval in patient_data.items():
                    setattr(user.patient_profile, subkey, subval)
            elif key == "doctor_profile":
                doctor_data = value
                if not user.doctor_profile:
                    raise ServiceError(f"User {id} has no doctor profile")
                for subkey, subval in doctor_data.items():
                    setattr(user.doctor_profile, subkey, subval)
        db.session.commit()

        # Invalidate caches
        cache.delete("users_list")
        cache.delete("doctors_list")
        cache.delete("appointments_list")
        cache.delete("patients_list")
        cache.delete_memoized(UserService.get_by_id, id)

        return user

    @staticmethod
    def delete(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ServiceError(f"User with id {id} not found")
        db.session.delete(user)
        db.session.commit()
        # Invalidate caches
        cache.delete("users_list")
        cache.delete("doctors_list")
        cache.delete("patients_list")
        cache.delete("appointments_list")
        cache.delete_memoized(UserService.get_by_id, id)
