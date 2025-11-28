from flask import request
from flask_restful import Resource, marshal, fields
from services import DocService
from flask_security import auth_required, roles_accepted, roles_required

from flask_restful import fields

from flask_restful import fields

specialization_fields = {
    "id": fields.Integer,
    "name": fields.String(attribute=lambda spec: spec.name if spec else "Unknown"),
    "description": fields.String(attribute=lambda spec: spec.description if spec else "")
}

credentials = {
    "id": fields.Integer(attribute=lambda doc: doc.user.id if doc.user else 0),
    "name": fields.String(attribute=lambda doc: doc.user.name if doc.user else "Unknown"),
    "email": fields.String(attribute=lambda doc: doc.user.email if doc.user else ""),
    "active": fields.Boolean(attribute=lambda doc: doc.user.active if doc.user else False)
}


doctor_fields = {
    "id": fields.Integer,
    "details": fields.Nested(credentials, attribute=lambda doc: doc),
    "specializations": fields.Nested(specialization_fields, attribute=lambda doc: doc.specialization_ref if doc else None),
    "availability": fields.Raw(attribute=lambda doc: doc.availability if doc else {}),
    "contact_number": fields.String(attribute=lambda doc: doc.contact_number if doc else ""),
    "created_at": fields.DateTime(attribute=lambda doc: doc.created_at if doc else None),
    "updated_at": fields.DateTime(attribute=lambda doc: doc.updated_at if doc else None)
}


class DoctorResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor', 'admin', 'patient')
    def get(self):
        uid= request.args.get("uid", type=int)
        id= request.args.get("id",type=int)

        if id:
            doc = DocService.get_by_id(id=id)
            return marshal(doc, doctor_fields), 200
        
        if uid:
            doc = DocService.get_by_id(uid=uid)
            return marshal(doc, doctor_fields), 200

    @auth_required('token')
    @roles_accepted('doctor', 'admin')
    def put(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.update(id,data,full_update=True)
        doc= DocService.get_by_id(id)
        return marshal(doc, doctor_fields), 200

    @auth_required('token')
    @roles_accepted('doctor', 'admin')
    def patch(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        data = request.get_json()
        DocService.update(id, data, full_update=False)
        doc= DocService.get_by_id(id)
        return marshal(doc, doctor_fields), 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        doc = DocService.get_by_id(id)
        if not doc:
            return {"message": "Doctor not found"}, 404
        DocService.delete(id)
        return {"message": "Doctor deleted successfully"}, 200
    


class DoctorListResource(Resource):
    @auth_required('token')
    @roles_accepted('doctor', 'admin','patient')
    def get(self):
        docs = DocService.get_all()
        return marshal(docs, doctor_fields), 200

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        print("RECEIVED: ",data)
        doc = DocService.create(data)
        return marshal(doc, doctor_fields), 201
