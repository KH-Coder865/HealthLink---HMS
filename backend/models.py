from extentions import db
from datetime import datetime, timezone
from flask_security.core import UserMixin, RoleMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship('Role', secondary='user_roles', backref='users')

    # parent → child cascades (useful)
    doctor_profile = db.relationship(
        "Doctor",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    patient_profile = db.relationship(
        "Patient",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Role(BaseModel, RoleMixin):
    __tablename__ = 'roles'
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class UserRoles(BaseModel):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

    doctors = db.relationship("Doctor", backref="specialization_ref", lazy=True)


class Doctor(BaseModel):
    __tablename__ = 'doctors'

    u_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # child → parent (cascade useless)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    availability = db.Column(db.JSON, nullable=True)
    contact_number = db.Column(db.String, nullable=True)

    appointments = db.relationship(
        "Appointment",
        backref="doctor",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Patient(BaseModel):
    __tablename__ = 'patients'

    u_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # child → parent (cascade useless)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)
    contact_number = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    emergency_contact = db.Column(db.String, nullable=True)

    appointments = db.relationship(
        "Appointment",
        backref="patient",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Appointment(BaseModel):
    __tablename__ = 'appointments'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, default='scheduled')

    treatment = db.relationship(
        "Treatment",
        backref="appointment",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Treatment(db.Model):
    __tablename__ = 'treatments'

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), primary_key=True)
    diagnosis = db.Column(db.Text, nullable=True)
    tests_done = db.Column(db.String, nullable=True)
    prescription = db.Column(db.JSON, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
