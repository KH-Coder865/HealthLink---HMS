import uuid
from models import User, db
from services.service_errors import ServiceError

class UserService:
    @staticmethod
    def get_by_id(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ServiceError(f"User with id {id} not found")
        return user

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def delete(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ServiceError(f"User with id {id} not found")
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def update(data):
        """{'id':1,'name':'new name',...}"""
        print(data["id"])
        user = User.query.filter_by(id=data.get("id")).first()
        if not user:
            raise ServiceError(f"User with id {data.get('id')} not found")
        
        allowed_keys = {"name", "email", "password", "active"}
    
        for key, value in data.items():
            if key in allowed_keys and key != "id":
                setattr(user, key, value)
        
        db.session.commit()

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
                patient_profile_data = value
                if not hasattr(user, "patient_profile") or not user.patient_profile:
                    raise ServiceError(f"User {id} has no patient profile")

                for subkey, subval in patient_profile_data.items():
                    setattr(user.patient_profile, subkey, subval)
            elif key == "doctor_profile":
                doctor_profile_data = value
                if not hasattr(user, "doctor_profile") or not user.doctor_profile:
                    raise ServiceError(f"User {id} has no doctor profile")

                for subkey, subval in doctor_profile_data.items():
                    setattr(user.doctor_profile, subkey, subval)
        
        db.session.commit()

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