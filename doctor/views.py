from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from doctor import models as doctor_models
from base import models as base_models


@login_required
def dashboard(request):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor, seen=False)
    paid_total = sum(
        b.total for b in base_models.Billing.objects.filter(appointment__doctor=doctor, status="Paid")
    )
    context = {
        "doctor": doctor,
        "appointments": appointments,
        "notifications": notifications,
        "paid_total": paid_total,
    }
    return render(request, "doctor/dashboard.html", context)


@login_required
def appointments(request):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    context = {"appointments": appointments}
    return render(request, "doctor/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }
    return render(request, "doctor/appointment_detail.html", context)


@login_required
def cancel_appointment(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "Cancelled"
    appointment.save()
    doctor_models.Notification.objects.create(
        doctor=doctor, appointment=appointment, type="Appointment Cancelled"
    )
    messages.success(request, "Appointment Cancelled Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "Scheduled"
    appointment.save()
    messages.success(request, "Appointment Re-Scheduled Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "Completed"
    appointment.save()
    messages.success(request, "Appointment Completed Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_medical_report(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        base_models.MedicalRecord.objects.create(
            appointment=appointment, diagnosis=diagnosis, treatment=treatment
        )
    messages.success(request, "Medical Report Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_medical_report(request, appointment_id, medical_report_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_report = base_models.MedicalRecord.objects.get(id=medical_report_id, appointment=appointment)
    if request.method == "POST":
        medical_report.diagnosis = request.POST.get("diagnosis")
        medical_report.treatment = request.POST.get("treatment")
        medical_report.save()
    messages.success(request, "Medical Report Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_lab_test(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        base_models.LabTest.objects.create(
            appointment=appointment,
            test_name=request.POST.get("test_name"),
            description=request.POST.get("description"),
            result=request.POST.get("result"),
        )
    messages.success(request, "Lab Test Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_lab_test(request, appointment_id, lab_test_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    lab_test = base_models.LabTest.objects.get(id=lab_test_id, appointment=appointment)
    if request.method == "POST":
        lab_test.test_name = request.POST.get("test_name")
        lab_test.description = request.POST.get("description")
        lab_test.result = request.POST.get("result")
        lab_test.save()
    messages.success(request, "Lab Test Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_prescription(request, appointment_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    if request.method == "POST":
        base_models.Prescription.objects.create(
            appointment=appointment,
            medications=request.POST.get("medications"),
        )
    messages.success(request, "Prescription Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_prescription(request, appointment_id, prescription_id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    prescription = base_models.Prescription.objects.get(id=prescription_id, appointment=appointment)
    if request.method == "POST":
        prescription.medications = request.POST.get("medications")
        prescription.save()
    messages.success(request, "Prescription Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def payments(request):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__doctor=doctor)
    context = {"payments": payments}
    return render(request, "doctor/payments.html", context)


@login_required
def notifications(request):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor)
    context = {"notifications": notifications}
    return render(request, "doctor/notifications.html", context)


@login_required
def mark_noti_seen(request, id):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    notification = doctor_models.Notification.objects.get(doctor=doctor, id=id)
    notification.seen = True
    notification.save()
    messages.success(request, "Notification marked as seen")
    return redirect("doctor:notifications")


@login_required
def profile(request):
    doctor, created = doctor_models.Doctor.objects.get_or_create(user=request.user)
    formatted_date = doctor.next_available_appointment_date.strftime('%Y-%m-%dT%H:%M') if doctor.next_available_appointment_date else ""
    if request.method == "POST":
        doctor.full_name = request.POST.get("full_name", doctor.full_name)
        doctor.mobile = request.POST.get("mobile", doctor.mobile)
        doctor.city = request.POST.get("city", doctor.city)
        doctor.state = request.POST.get("state", doctor.state)
        doctor.bio = request.POST.get("bio", doctor.bio)
        doctor.specialization = request.POST.get("specialization", doctor.specialization)
        doctor.qualifications = request.POST.get("qualifications", doctor.qualifications)
        doctor.years_of_experience = request.POST.get("years_of_experience", doctor.years_of_experience)
        doctor.registration_number = request.POST.get("registration_number", doctor.registration_number)
        next_date = request.POST.get("next_available_appointment_date")
        if next_date:
            doctor.next_available_appointment_date = next_date
        if request.FILES.get("image"):
            doctor.image = request.FILES["image"]
        doctor.save()
        messages.success(request, "Profile updated successfully")
        return redirect("doctor:profile")
    context = {
        "doctor": doctor,
        "formatted_next_available_appointment_date": formatted_date,
    }
    return render(request, "doctor/profile.html", context)
