from celery import shared_task 
from models import Appointment, Patient
from services import AppointmentService
import os, csv
import datetime

@shared_task(ignore_results=False, name='csv_report')
def csv_report(patient_id):
    appointments = AppointmentService.get_pat_hist(patient_id)
    if not appointments:
        return None

    csv_file_name = f"patient_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    static_path = os.path.join("static", "csv_exports")
    os.makedirs(static_path, exist_ok=True)
    full_path = os.path.join(static_path, csv_file_name)

    with open(full_path, mode='w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sr No", "Appointment Date", "Doctor Name", "Department", "Tests", "Diagnosis", "Prescription", "Notes"])
        for i, appt in enumerate(appointments, start=1):
            writer.writerow([
                i,
                appt['date'],
                appt['doctor'],
                appt['dept'],
                appt['tests_done'] if appt['tests_done'] else "",
                appt['diagnosis'] if appt['diagnosis'] else "",
                appt['prescription'] if appt['prescription'] else "",
                appt['notes'] if appt['notes'] else ""
            ])

    # Return the download URL
    download_url = f"/download_csv/{csv_file_name}"
    return download_url


@shared_task(ignore_results = False, name = "monthly_report")
def monthly_report():
    return "Monthly reports sent"

@shared_task(ignore_results = False, name = "appt_notify")
def appt_notify():
    return "Appointment notifications initiated"
