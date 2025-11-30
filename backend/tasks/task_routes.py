from flask import Blueprint
from flask import jsonify
from .tasks import csv_report
from celery.result import AsyncResult

bp = Blueprint("tasks", __name__)

@bp.route('/api/export/<int:patient_id>')
def export_csv(patient_id):
    result = csv_report.delay(patient_id)
    return jsonify({
        "task_id": result.id,
        "status": "started"
    })

@bp.route('/api/csv_result/<task_id>')
def csv_result(task_id):
    result = AsyncResult(task_id)
    return {
        "ready": result.ready(),
        "url": result.result if result.ready() else None
    }
