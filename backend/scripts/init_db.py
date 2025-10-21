

from app import app
from models import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
    db.drop_all()
    db.create_all()
    datastore : SQLAlchemyUserDatastore=app.datastore
    admin_role  = datastore.find_or_create_role("admin", description="super user")
    doctor_role = datastore.find_or_create_role("doctor", description= "treats patient and sets availability")
    patient_role = datastore.find_or_create_role("patient", description = "seeks medical assistance by scheduling appointment")

    if not datastore.find_user(email="kaushik@admin.com"):
        datastore.create_user(
            email="kaushik@admin.com",
            name="Kaushik",
            password= hash_password("1234")
        )
    
    if not datastore.find_user(email="u1@doctor.com"):
        datastore.create_user(
            email="u1@doctor.com",
            name="Doctor_01",
            password= hash_password("1234")
        )

    if not datastore.find_user(email="u2@patient.com"):
        datastore.create_user(
            email="u2@patient.com",
            name="Patient_01",
            password= hash_password("1234")
        )


    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    admin=datastore.find_user(email="kaushik@admin.com")
    doc=datastore.find_user(email="u1@doctor.com")
    pat=datastore.find_user(email="u2@patient.com")

    admin_role=datastore.find_role("admin")
    doctor_role=datastore.find_role("doctor")
    patient_role=datastore.find_role("patient")

    datastore.add_role_to_user(admin,admin_role)
    datastore.add_role_to_user(doc,doctor_role)
    datastore.add_role_to_user(pat,patient_role)

    try:
        db.session.commit()
        print("✅")
    except:
        db.session.rollback()
        print("❌")