from flask import current_app
import requests
from flask_mail import Message
from extentions import mail
from celery import shared_task
from models import Appointment
from utils import format_report
from services import AppointmentService, DocService
import os, csv
import pdfkit
import datetime


@shared_task(ignore_results=False, name='csv_report')
def csv_report(patient_id):
    with current_app.app_context():
        appointments = AppointmentService.get_pat_hist(patient_id)
        if not appointments:
            return None

        csv_file_name = f"patient_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        static_path = os.path.join("static", "csv_exports")
        os.makedirs(static_path, exist_ok=True)
        full_path = os.path.join(static_path, csv_file_name)

        with open(full_path, mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Sr No", "Appointment Date", "Doctor Name", "Department", "Tests",
                             "Diagnosis", "Prescription", "Notes"])
            for i, appt in enumerate(appointments, start=1):
                writer.writerow([
                    i,
                    appt['date'],
                    appt['doctor'],
                    appt['dept'],
                    appt['tests_done'] or "",
                    appt['diagnosis'] or "",
                    appt['prescription'] or "",
                    appt['notes'] or ""
                ])

        download_url = f"/download_csv/{csv_file_name}"
        return download_url


@shared_task(ignore_results=False, name="send_pdf_email")
def send_pdf_email(recipient_email, subject, body, pdf_file_path):
    with current_app.app_context():
        msg = Message(
            subject=subject,
            recipients=[recipient_email]
        )
        msg.body = body

        with open(pdf_file_path, 'rb') as f:
            msg.attach(
                filename=os.path.basename(pdf_file_path),
                content_type='application/pdf',
                data=f.read()
            )

        try:
            mail.send(msg)
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")


def serialize_appt(a):
    """Convert SQLAlchemy object into a safe dict for Jinja."""
    return {
        "patient": a.patient.user.name if a.patient and a.patient.user else "",
        "date": a.appointment_date.strftime("%d-%m-%Y"),
        "status": a.status,

        "tests": a.treatment.tests_done if a.treatment else "",
        "diagnosis": a.treatment.diagnosis if a.treatment else "",

        "prescriptions": [
            {
                "med": p["med"],
                "dose": p["dose"],
                "duration": p["duration"]
            }
            for p in (a.treatment.prescription if a.treatment and a.treatment.prescription else [])
        ]
    }



from celery import shared_task
from flask import current_app
from models import Appointment
from services import DocService
from tasks.tasks import serialize_appt, format_report, send_pdf_email
import datetime, os, pdfkit
import calendar

@shared_task(ignore_results=False, name="monthly_report_all")
def monthly_report_all():
    with current_app.app_context():
        today = datetime.date.today()
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1

        first_day_prev_month = datetime.date(prev_year, prev_month, 1)
        last_day_prev_month = datetime.date(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1])

        all_doctors = DocService.get_all()

        reports_dir = os.path.join("static", "monthly_reports")
        os.makedirs(reports_dir, exist_ok=True)

        for doctor in all_doctors:
            # Query appointments for previous month
            raw_appts = Appointment.query.filter(
                Appointment.appointment_date >= first_day_prev_month,
                Appointment.appointment_date <= last_day_prev_month,
                Appointment.doctor_id == doctor.id
            ).all()

            if not raw_appts:
                continue

            appts = [serialize_appt(a) for a in raw_appts]

            data = {
                "doctor": doctor.user.name,
                "from_date": str(first_day_prev_month),
                "to_date": str(last_day_prev_month),
                "appts": appts
            }

            html = format_report("templates/report.html", data)

            pdf_file = os.path.join(
                reports_dir,
                f"monthly_report_{doctor.id}_{today.strftime('%Y%m%d_%H%M%S')}.pdf"
            )

            pdfkit.from_string(html, pdf_file)

            send_pdf_email.delay(
                recipient_email=os.environ.get("recepem"),
                subject=f"Monthly Report - {doctor.user.name}",
                body="Dear Doctor,\n\nPlease find your monthly report attached.",
                pdf_file_path=pdf_file
            )

        return "Monthly reports tasks triggered."



PATIENT_GCHAT_WEBHOOK = os.environ.get("PATIENT_GCHAT_WEBHOOK")
DOCTOR_GCHAT_WEBHOOK = os.environ.get("DOCTOR_GCHAT_WEBHOOK")

@shared_task(ignore_results=False, name="appt_notify")
def appt_notify():
    with current_app.app_context():
        today = datetime.date.today()

        # Fetch all today's appointments
        todays_appts = Appointment.query.filter(
            Appointment.appointment_date == today
        ).all()

        if not todays_appts:
            return "No appointments today"

        sent_count = 0

        for appt in todays_appts:
            patient_name = appt.patient.user.name if appt.patient and appt.patient.user else "Patient"
            doctor_name = appt.doctor.user.name if appt.doctor and appt.doctor.user else "Doctor"

            # Combine date + time for display
            time_str = appt.appointment_time.strftime("%H:%M") if appt.appointment_time else "N/A"

            # Message to patient
            if PATIENT_GCHAT_WEBHOOK:
                patient_msg = {
                    "text": f"Hello {patient_name}, you have an appointment today at {time_str} with Dr. {doctor_name}."
                }
                try:
                    requests.post(PATIENT_GCHAT_WEBHOOK, json=patient_msg)
                    sent_count += 1
                except Exception as e:
                    current_app.logger.error(f"Failed to send patient notification: {e}")

            # Message to doctor
            if DOCTOR_GCHAT_WEBHOOK:
                doctor_msg = {
                    "text": f"Hello Dr. {doctor_name}, you have an appointment today at {time_str} with {patient_name}."
                }
                try:
                    requests.post(DOCTOR_GCHAT_WEBHOOK, json=doctor_msg)
                    sent_count += 1
                except Exception as e:
                    current_app.logger.error(f"Failed to send doctor notification: {e}")

        return f"Sent {sent_count} notifications"