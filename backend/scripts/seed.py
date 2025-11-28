import random
import uuid
from datetime import datetime, timedelta, time, timezone
from faker import Faker
from faker_food import FoodProvider
from flask_security.utils import hash_password

from app import create_app
from models import db, User, Role, UserRoles, Doctor, Patient, Specialization, Appointment, Treatment

# --- Faker Setup ---
fake = Faker()
fake.add_provider(FoodProvider)

def indian_phone_number():
    return f"+91-{random.randint(6000000000, 9999999999)}"

def random_time_slot():
    """Return a time in either 09:00–12:00 or 16:00–21:00 using 15-minute intervals."""
    if random.random() < 0.5:
        hour = random.choice([9, 10, 11, 12])
    else:
        hour = random.choice([16, 17, 18, 19, 20, 21])
    minute = random.choice([0, 15, 30, 45])
    return time(hour, minute)

def make_genuine_timestamps(appointment_dt, now_dt):
    if appointment_dt < now_dt:
        created_before = random.randint(1, 60)
        created_at = appointment_dt - timedelta(days=created_before, hours=random.randint(0, 12), minutes=random.randint(0,59))
    else:
        created_before = random.randint(0, 14)
        created_at = now_dt - timedelta(days=created_before, hours=random.randint(0, 12), minutes=random.randint(0,59))
    if created_at > now_dt:
        created_at = now_dt - timedelta(minutes=random.randint(0, 60))
    updated_at = created_at
    return created_at, updated_at

app = create_app()

with app.app_context():
    print("🔄 Resetting database...")
    db.drop_all()
    db.create_all()

    print("🧩 Creating roles...")
    admin_role = Role(name="admin", description="Administrator with full access")
    doctor_role = Role(name="doctor", description="Doctor user with limited admin access")
    patient_role = Role(name="patient", description="General patient user")
    db.session.add_all([admin_role, doctor_role, patient_role])
    db.session.commit()

    print("👑 Creating admin user...")
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

    print("🏥 Creating specializations...")
    specialization_data = [
        (
            "Cardiology",
            "Cardiology focuses on disorders of the heart and blood vessels. This department "
            "manages conditions such as coronary artery disease, arrhythmias, heart failure, "
            "valvular heart disease, and hypertension. Cardiologists provide diagnostic tests "
            "including ECG, echocardiograms, stress tests, and angiography, and offer both "
            "medical and interventional treatments to improve cardiovascular health."
        ),
        (
            "Neurology",
            "Neurology is dedicated to diagnosing and treating disorders of the brain, spinal cord, "
            "and peripheral nerves. Neurologists manage conditions like epilepsy, migraines, stroke, "
            "Parkinson’s disease, neuropathies, and multiple sclerosis. Care includes neurological "
            "exams, imaging studies, electrophysiological testing, and long-term management of "
            "chronic neurological illnesses."
        ),
        (
            "Pediatrics",
            "Pediatrics deals with the medical care of infants, children, and adolescents. Pediatricians "
            "provide preventive care, routine vaccinations, developmental monitoring, and treatment "
            "of infections, allergies, nutritional issues, and childhood disorders. The department "
            "focuses on both the physical and emotional well-being of children at all stages of growth."
        ),
        (
            "Orthopedics",
            "Orthopedics specializes in the diagnosis and treatment of musculoskeletal conditions "
            "including fractures, joint problems, arthritis, sports injuries, spinal disorders, and "
            "congenital deformities. Treatment options include physical therapy, medications, minimally "
            "invasive procedures, and surgical interventions such as joint replacement."
        ),
        (
            "Dermatology",
            "Dermatology handles diseases of the skin, hair, and nails. This includes acne, eczema, "
            "psoriasis, fungal infections, pigmentation issues, and skin cancers. Dermatologists "
            "provide both medical and cosmetic treatments including laser therapy, biopsies, and "
            "advanced skincare procedures tailored to individual needs."
        ),
        (
            "Psychiatry",
            "Psychiatry is concerned with the diagnosis, treatment, and prevention of mental, emotional, "
            "and behavioral disorders. Psychiatrists manage depression, anxiety, bipolar disorder, "
            "schizophrenia, trauma-related disorders, and substance-use problems using therapy, "
            "counseling, and medications tailored to each patient."
        ),
        (
            "Ophthalmology",
            "Ophthalmology deals with eye and vision care. This includes diagnosing and treating "
            "cataracts, glaucoma, refractive errors, retinal disorders, infections, and trauma. "
            "Ophthalmologists perform vision assessments, prescribe corrective lenses, and offer "
            "medical or surgical eye treatments."
        ),
        (
            "Oncology",
            "Oncology focuses on the diagnosis and treatment of cancer. Oncologists specialize in "
            "medical, radiation, and surgical treatments depending on the cancer type. The department "
            "also manages chemotherapy, immunotherapy, targeted therapy, and cancer follow-ups, as well "
            "as providing supportive and palliative care."
        ),
        (
            "Radiology",
            "Radiology uses advanced imaging techniques to diagnose and monitor diseases. Specialists "
            "interpret X-rays, CT scans, MRI scans, ultrasounds, and PET scans. Radiologists support "
            "nearly every medical department by providing accurate imaging-based diagnosis and "
            "image-guided procedures."
        ),
        (
            "General Medicine",
            "General Medicine provides primary care services, managing common illnesses, infections, "
            "chronic diseases like diabetes and hypertension, and overall preventive healthcare. "
            "Internal medicine physicians evaluate symptoms, order diagnostic tests, and coordinate "
            "with specialty departments when necessary."
        ),
    ]

    specializations = []
    for name, desc in specialization_data:
        sp = Specialization(name=name, description=desc)
        db.session.add(sp)
        specializations.append(sp)
    db.session.commit()

    print("🩺 Creating doctors...")
    doctors = []
    for i in range(20):
        user = User(
            name=fake.name(),
            email=f"doctor{i+1}@hospital.com",
            password=hash_password("1234"),
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(UserRoles(user_id=user.id, role_id=doctor_role.id))

        specialization = random.choice(specializations)
        today = datetime.now().date()
        availability = {}

        for k in range(7):
            d = today + timedelta(days=k)
            key = d.strftime("%Y-%m-%d")
            availability[key] = {
                "morning": 0,
                "evening": 0
            }

        doctor = Doctor(
            u_id=user.id,
            specialization_id=specialization.id,
            availability=availability,
            contact_number=indian_phone_number()
        )
        db.session.add(doctor)
        doctors.append(doctor)

    db.session.commit()

    print("🧍 Creating patients...")
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

    print("📅 Creating appointments and treatments...")
    now_utc = datetime.now(timezone.utc)
    doctor_schedule = {doc.id: {} for doc in doctors}  # track doctor appointments

    def get_unique_appointment(doctor_id, start_date, end_date):
        """Generate a time slot that does not collide with existing appointments of the doctor."""
        date = start_date
        while date <= end_date:
            if date not in doctor_schedule[doctor_id]:
                doctor_schedule[doctor_id][date] = set()
            available_slots = []
            for h in range(9,13):
                for m in [0,15,30,45]:
                    available_slots.append(time(h,m))
            for h in range(16,22):
                for m in [0,15,30,45]:
                    available_slots.append(time(h,m))
            free_slots = [t for t in available_slots if t not in doctor_schedule[doctor_id][date]]
            if free_slots:
                chosen_time = random.choice(free_slots)
                doctor_schedule[doctor_id][date].add(chosen_time)
                return date, chosen_time
            date += timedelta(days=1)
        # fallback
        return start_date, time(9,0)

    # create past completed appointments
    for patient in patients:
        doctor = random.choice(doctors)  # choose doctor once per patient
        completed_date = now_utc.date() - timedelta(days=random.randint(1,180))
        completed_date, completed_time = get_unique_appointment(doctor.id, completed_date, completed_date)
        completed_dt = datetime.combine(completed_date, completed_time).replace(tzinfo=timezone.utc)
        created_at, updated_at = make_genuine_timestamps(completed_dt, now_utc)

        appt = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            appointment_date=completed_date,
            appointment_time=completed_time,
            status="completed",
            created_at=created_at,
            updated_at=updated_at
        )
        db.session.add(appt)
        db.session.flush()

        treatment = Treatment(
            appointment_id=appt.id,
            diagnosis=random.choice(["Common Cold", "Hypertension", "Migraine", "Diabetes"]),
            prescription=[{"med": fake.word().capitalize(), "dose": f"{random.randint(50,500)}mg", "duration": f"{random.randint(3,10)} days", "timing":"1-0-1"}],
            tests_done=random.choice(["ECG","MRI","Blood Test","None"]),
            notes=fake.paragraph(nb_sentences=3),
            created_at=created_at,
            updated_at=updated_at
        )
        db.session.add(treatment)

        # create future scheduled appointment for the SAME doctor
        start_date = now_utc.date() + timedelta(days=1)
        end_date = now_utc.date() + timedelta(days=7)
        scheduled_date, scheduled_time = get_unique_appointment(doctor.id, start_date, end_date)
        scheduled_dt = datetime.combine(scheduled_date, scheduled_time).replace(tzinfo=timezone.utc)
        created_at, updated_at = make_genuine_timestamps(scheduled_dt, now_utc)

        appt = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            appointment_date=scheduled_date,
            appointment_time=scheduled_time,
            status="scheduled",
            created_at=created_at,
            updated_at=updated_at
        )
        db.session.add(appt)


    db.session.commit()
    print("✅ Database successfully seeded with Admin, Doctors, Patients, Appointments & Treatments.")
