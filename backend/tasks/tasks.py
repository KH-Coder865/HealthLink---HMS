from flask import current_app
from flask_mail import Message
from app import mail
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


@shared_task(ignore_results=False, name="monthly_report_all")
def monthly_report_all():
    with current_app.app_context():
        tod = datetime.date.today()
        fday = tod.replace(day=1)
        all_doctors = DocService.get_all()

        reports_dir = os.path.join("static", "monthly_reports")
        os.makedirs(reports_dir, exist_ok=True)

        for doctor in all_doctors:
            appts = Appointment.query.filter(
                Appointment.appointment_date >= fday,
                Appointment.appointment_date <= tod,
                Appointment.doctor_id == doctor.id
            ).all()

            if not appts:
                continue

            data = {
                "doctor": doctor.user.name,
                "from_date": str(fday),
                "to_date": str(tod),
                "appts": appts
            }

            html = format_report("templates/report.html", data)
            pdf_file = os.path.join(
                reports_dir,
                f"monthly_report_{doctor.id}_{tod.strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            pdfkit.from_string(html, pdf_file)

            send_pdf_email.delay(
                recipient_email='hariharsha153@gmail.com',
                subject=f"Monthly Report - {data['doctor']}",
                body="Dear Doctor,\n\nPlease find your monthly report attached.",
                pdf_file_path=pdf_file
            )

        return "Monthly reports tasks triggered."


@shared_task(ignore_results=False, name="appt_notify")
def appt_notify():
    return "Appointment notifications initiated"
