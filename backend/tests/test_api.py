
"""
HealthLink HMS - Backend API Test Suite

Tests:
1. User registration
2. Input validation
3. Duplicate user prevention
4. Authentication
5. Invalid credentials
6. Token-based authorization
7. Protected API access
8. Appointment API access
9. Specialization API access
10. Treatment API access
"""

import pytest

from app import app as flask_app
from extentions import db
from models import Role


@pytest.fixture(scope="session")
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret-key",
        SECURITY_PASSWORD_SALT="test-password-salt",
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()

        # Initialize roles required by Flask-Security
        for role_name in ["admin", "doctor", "patient"]:
            if not flask_app.datastore.find_role(role_name):
                flask_app.datastore.create_role(name=role_name)

        db.session.commit()

        yield flask_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def patient(client):
    """Create a patient and return registration details."""

    payload = {
        "name": "Test Patient",
        "email": "patient_test@healthlink.com",
        "password": "StrongPassword@123",
        "role": "patient",
        "age": 25,
        "gender": "Male",
        "contact_number": "9876543210",
        "address": "Test City",
        "emergency_contact": "9876543211",
    }

    response = client.post(
        "/api/auth/register",
        json=payload
    )

    assert response.status_code == 201

    return payload


@pytest.fixture
def patient_token(client, patient):
    """Authenticate patient and return access token."""

    response = client.post(
        "/api/auth/login",
        json={
            "email": patient["email"],
            "password": patient["password"],
        },
    )

    assert response.status_code == 200

    return response.get_json()["token"]


# --------------------------------------------------
# 1. APPLICATION TESTS
# --------------------------------------------------

def test_application_initialization(app):
    assert app is not None
    assert app.testing is True


def test_api_routes_are_registered(app):
    routes = [
        rule.rule for rule in app.url_map.iter_rules()
    ]

    assert "/api/auth/register" in routes
    assert "/api/auth/login" in routes
    assert "/api/appointments" in routes
    assert "/api/patients" in routes
    assert "/api/doctors" in routes


# --------------------------------------------------
# 2. USER REGISTRATION TESTS
# --------------------------------------------------

def test_patient_registration(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Alice Johnson",
            "email": "alice@healthlink.com",
            "password": "SecurePass@123",
            "role": "patient",
            "age": 28,
            "gender": "Female",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["email"] == "alice@healthlink.com"
    assert data["role"] == "patient"
    assert data["active"] is True
    assert "token" in data


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"name": "John"},
        {
            "name": "John",
            "email": "john@healthlink.com",
        },
        {
            "name": "John",
            "email": "john@healthlink.com",
            "password": "password123",
        },
    ],
)
def test_registration_with_missing_fields(client, payload):
    response = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert response.status_code == 400


def test_admin_registration_is_rejected(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Unauthorized Admin",
            "email": "fakeadmin@healthlink.com",
            "password": "Password123",
            "role": "admin",
        },
    )

    assert response.status_code == 400


def test_duplicate_registration(client, patient):
    response = client.post(
        "/api/auth/register",
        json=patient,
    )

    assert response.status_code == 400


def test_doctor_registration(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Dr. Test",
            "email": "doctor_test@healthlink.com",
            "password": "DoctorPass@123",
            "role": "doctor",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["active"] is False


# --------------------------------------------------
# 3. LOGIN AND AUTHENTICATION TESTS
# --------------------------------------------------

def test_valid_patient_login(client, patient):
    response = client.post(
        "/api/auth/login",
        json={
            "email": patient["email"],
            "password": patient["password"],
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["email"] == patient["email"]
    assert data["role"] == "patient"
    assert data["token"]


def test_invalid_password(client, patient):
    response = client.post(
        "/api/auth/login",
        json={
            "email": patient["email"],
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_nonexistent_user_login(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@healthlink.com",
            "password": "SomePassword",
        },
    )

    assert response.status_code == 404


# --------------------------------------------------
# 4. TOKEN AUTHORIZATION TESTS
# --------------------------------------------------

@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/users",
        "/api/doctors",
        "/api/patients",
        "/api/appointments",
        "/api/specializations",
    ],
)
def test_protected_endpoints_reject_unauthenticated_users(
    client, endpoint
):
    response = client.get(endpoint)

    assert response.status_code in (401, 403)


def test_patient_can_access_appointment_list(
    client, patient_token
):
    response = client.get(
        "/api/appointments",
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 200


def test_patient_can_access_patient_list(
    client, patient_token
):
    response = client.get(
        "/api/patients",
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 200


# --------------------------------------------------
# 5. APPOINTMENT API TESTS
# --------------------------------------------------

def test_appointment_query_requires_identifier(
    client, patient_token
):
    response = client.get(
        "/api/appointment",
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 400


def test_nonexistent_appointment_returns_not_found(
    client, patient_token
):
    response = client.patch(
        "/api/appointments/999999",
        json={"status": "cancelled"},
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 404


def test_deleting_nonexistent_appointment(
    client, patient_token
):
    response = client.delete(
        "/api/appointments/999999",
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 404


# --------------------------------------------------
# 6. SPECIALIZATION API TESTS
# --------------------------------------------------

def test_specialization_query_requires_identifier(
    client, patient_token
):
    response = client.get(
        "/api/specialization",
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code == 400


# --------------------------------------------------
# 7. TREATMENT API TESTS
# --------------------------------------------------

def test_treatment_creation_requires_doctor_role(
    client, patient_token
):
    response = client.post(
        "/api/treatments",
        json={
            "appointment_id": 1,
            "diagnosis": "General Checkup",
            "tests_done": "Blood Test",
            "prescription": {
                "medicine": "Test Medicine",
                "dosage": "1 tablet",
            },
            "notes": "Routine checkup",
        },
        headers={
            "Authentication-Token": patient_token
        },
    )

    assert response.status_code in (401, 403)


def test_treatment_list_requires_authentication(client):
    response = client.get("/api/treatments")

    assert response.status_code in (401, 403)


# --------------------------------------------------
# 8. RESPONSE FORMAT TESTS
# --------------------------------------------------

def test_login_response_contains_required_fields(
    client, patient
):
    response = client.post(
        "/api/auth/login",
        json={
            "email": patient["email"],
            "password": patient["password"],
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    required_fields = [
        "id",
        "name",
        "email",
        "role",
        "active",
        "token",
    ]

    for field in required_fields:
        assert field in data


def test_invalid_json_registration(client):
    response = client.post(
        "/api/auth/register",
        data="invalid-json",
        content_type="application/json",
    )

    assert response.status_code == 400
