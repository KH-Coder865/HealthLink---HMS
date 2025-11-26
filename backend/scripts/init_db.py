import random
import uuid
from datetime import datetime, timedelta, time
from faker import Faker
from faker_food import FoodProvider
from flask_security.utils import hash_password

from app import create_app
from models import db, User, Role, UserRoles, Doctor, Patient, Specialization, Appointment, Treatment

# Initialize Faker
fake = Faker()
fake.add_provider(FoodProvider)

def indian_phone_number():
    """Generate Indian-style +91 formatted phone number"""
    return f"+91-{random.randint(6000000000, 9999999999)}"

app = create_app()

with app.app_context():
    print("Resetting database...")
    db.drop_all()
    db.create_all()

    # --- Create roles ---
    print("Creating roles...")
    admin_role = Role(name="admin", description="Administrator with full access")
    doctor_role = Role(name="doctor", description="Doctor user with limited admin access")
    patient_role = Role(name="patient", description="General patient user")
    db.session.add_all([admin_role, doctor_role, patient_role])
    db.session.commit()

    # --- Create admin user ---
    print("Creating admin user...")
    admin_user = User(
        name="Admin User",
        email="admin@hospital.com",
        password=hash_password("1234"),
        fs_uniquifier=str(uuid.uuid4())
    )
    db.session.add(admin_user)
    db.session.commit()

    db.session.add(UserRoles(user_id=admin_user.id, role_id=admin_role.id))
    db.session.commit()

    # --- Create Specializations ---
    print("Creating specializations...")
    specialization_names = [
        ("Cardiology", "Heart and blood vessel specialists."),
        ("Neurology", "Brain and nervous system specialists."),
        ("Pediatrics", "Child and adolescent care."),
        ("Orthopedics", "Bone and joint specialists."),
        ("Dermatology", "Skin care specialists."),
        ("Psychiatry", "Mental health professionals."),
        ("Ophthalmology", "Eye and vision specialists."),
        ("Oncology", "Cancer specialists."),
        ("Radiology", "Medical imaging experts."),
        ("General Medicine", "General health practitioners."),
    ]

    specializations = []
    for name, desc in specialization_names:
        sp = Specialization(name=name, description=desc)
        db.session.add(sp)
        specializations.append(sp)
    db.session.commit()

    # --- Create doctors ---
    print("Creating doctors...")
    doctors = []
    for i in range(10):
        user = User(
            name=fake.name(),
            email=f"doctor{i+1}@hospital.com",
            password=hash_password("1234"),
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(user)
        db.session.flush()  # assign id
        db.session.add(UserRoles(user_id=user.id, role_id=doctor_role.id))

        specialization = random.choice(specializations)
        availability = {
            day: [f"{random.randint(8, 16)}:00", f"{random.randint(17, 20)}:00"]
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        }
        doctor = Doctor(
            u_id=user.id,
            specialization_id=specialization.id,
            availability=availability,
            contact_number=indian_phone_number()  # added field
        )
        db.session.add(doctor)
        doctors.append(doctor)
    db.session.commit()

    # --- Create patients ---
    print("Creating patients...")
    genders = ["Male", "Female", "Other"]
    patients = []
    for i in range(50):
        user = User(
            name=fake.name(),
            email=f"patient{i+1}@hospital.com",
            password=hash_password("1234"),
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(UserRoles(user_id=user.id, role_id=patient_role.id))

        patient = Patient(
            u_id=user.id,
            age=random.randint(10, 80),
            gender=random.choice(genders),
            contact_number=indian_phone_number(),
            address=fake.address(),
            emergency_contact=indian_phone_number()
        )
        db.session.add(patient)
        patients.append(patient)
    db.session.commit()

    # --- Create appointments and treatments ---
    print("Creating appointments and treatments...")
    statuses = ["scheduled", "completed", "cancelled"]
    for _ in range(200):  # 200 appointments total
        doctor = random.choice(doctors)
        patient = random.choice(patients)

        # random date over last 6 months
        days_ago = random.randint(0, 180)
        appt_date = datetime.now().date() - timedelta(days=days_ago)
        appt_time = time(random.randint(8, 18), random.choice([0, 15, 30, 45]))
        status = random.choices(statuses, weights=[0.3, 0.6, 0.1])[0]

        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            status=status
        )
        db.session.add(appointment)
        db.session.flush()

        if status == "completed":
            # Create a treatment record for completed appointments
            diagnosis = random.choice([
                "Common Cold", "Hypertension", "Allergic Rhinitis",
                "Migraine", "Type 2 Diabetes", "Anxiety Disorder",
                "Back Pain", "Asthma", "Gastritis", "Arthritis"
            ])
            prescription = [
                {
                    "med": fake.sentence(nb_words=1).strip('.'),
                    "dose": f"{random.randint(100, 500)}mg",
                    "duration": f"{random.randint(3, 10)} days"
                },
                {
                    "med": fake.dish(),
                    "dose": "Diet Recommendation",
                    "duration": "Lifestyle"
                }
            ]
            treatment = Treatment(
                appointment_id=appointment.id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=fake.paragraph(nb_sentences=3)
            )
            db.session.add(treatment)

    db.session.commit()
    print("✅ Database successfully seeded with roles, users, doctors, patients, appointments, and treatments.")
