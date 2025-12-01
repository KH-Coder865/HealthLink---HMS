from flask import Blueprint
from flask import jsonify
from .tasks import csv_report, monthly_report_all, appt_notify
from celery.result import AsyncResult

bp = Blueprint("tasks", __name__, url_prefix="/api")

@bp.route('/reports/send')
def send_reports():
    result = monthly_report_all.delay()
    return jsonify({
        "task_id": result.id,
        "status": "started"
    })

@bp.route('/appts/notify')
def notify_appointments():
    result = appt_notify.delay()
    return jsonify({
        "task_id": result.id,
        "status": "started"
    })


@bp.route('/export/<int:patient_id>')
def export_csv(patient_id):
    result = csv_report.delay(patient_id)
    return jsonify({
        "task_id": result.id,
        "status": "started"
    })



@bp.route('/csv_result/<task_id>')
def csv_result(task_id):
    result = AsyncResult(task_id)
    return {
        "ready": result.ready(),
        "url": result.result if result.ready() else None
    }
