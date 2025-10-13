from .extentions import db
from datetime import datetime, timezone

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class User(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="patient")  # "admin", "doctor", "patient"

    # Relationships
    doctor_profile = db.relationship("Doctor", backref="user", uselist=False)
    patient_profile = db.relationship("Patient", backref="user", uselist=False)


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

    # Relationships
    doctors = db.relationship("Doctor", backref="specialization_ref", lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # FK to User
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    availability = db.Column(db.JSON, nullable=True)  # Store availability as JSON (e.g., {"Monday": ["10:00", "14:00"]})

    # Relationships
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # FK to User
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)
    contact_number = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    emergency_contact = db.Column(db.String, nullable=True)

    # Relationships
    appointments = db.relationship("Appointment", backref="patient", lazy=True)



class Appointment(BaseModel):
    __tablename__ = 'appointments'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, default='scheduled')  # scheduled, completed, cancelled

    # Relationships
    treatment = db.relationship("Treatment", backref="appointment", uselist=False)



class Treatment(BaseModel):
    __tablename__ = 'treatments'

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), primary_key=True)
    diagnosis = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.JSON, nullable=True)  # Store as JSON: [{"med": "Paracetamol", "dose": "500mg", "duration": "5 days"}]
    notes = db.Column(db.Text, nullable=True)
