from flask import Blueprint
from flask_restful import Api

from resources.auth import auth_bp

from resources.user_resource import UserResource, UserListResource
from resources.doctor_resource import DoctorResource, DoctorListResource
from resources.patient_resource import PatientResource, PatientListResource
from resources.appointment_resource import AppointmentResource, AppointmentListResource
from resources.treatment_resource import TreatmentResource, TreatmentListResource
from resources.specialization_resource import SpecializationResource, SpecializationListResource

# Create main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# User
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')

# Doctor
api.add_resource(DoctorListResource, '/doctors')
api.add_resource(DoctorResource, '/doctors/<int:id>',endpoint='doc_by_id')
api.add_resource(DoctorResource, '/doctor',endpoint='doc_by_query')

# Patient
api.add_resource(PatientListResource, '/patients')
api.add_resource(PatientResource, '/patients/<int:id>')

# Appointment
api.add_resource(AppointmentListResource, '/appointments')
api.add_resource(AppointmentResource, '/appointments/<int:id>', endpoint="appt_by_id")
api.add_resource(AppointmentResource, '/appointment',endpoint="appt_by_query")

# Treatment
api.add_resource(TreatmentListResource, '/treatments')
api.add_resource(TreatmentResource, '/treatments/<int:appointment_id>')

# Specialization
api.add_resource(SpecializationListResource, '/specializations')
api.add_resource(SpecializationResource, '/specializations/<int:id>', endpoint="spec_by_id")
api.add_resource(SpecializationResource, '/specialization', endpoint="spec_by_query")