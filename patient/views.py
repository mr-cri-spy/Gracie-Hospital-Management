from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from patient import models as patient_models
from base import models as base_models


@login_required
def dashboard(request):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    total_spent = sum(
        b.total for b in base_models.Billing.objects.filter(patient=patient, status="Paid")
    )
    context = {
        "patient": patient,
        "appointments": appointments,
        "notifications": notifications,
        "total_spent": total_spent,
    }
    return render(request, "patient/dashboard.html", context)


@login_required
def appointments(request):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    context = {"appointments": appointments, "patient": patient}
    return render(request, "patient/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    billing = base_models.Billing.objects.filter(appointment=appointment).first()
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "billing": billing,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
        "patient": patient,
    }
    return render(request, "patient/appointment_detail.html", context)


@login_required
def cancel_appointment(request, appointment_id):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Cancelled"
    appointment.save()
    patient_models.Notification.objects.create(
        patient=patient, appointment=appointment, type="Appointment Cancelled"
    )
    messages.success(request, "Appointment Cancelled Successfully")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Scheduled"
    appointment.save()
    messages.success(request, "Appointment Re-Scheduled Successfully")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Completed"
    appointment.save()
    messages.success(request, "Appointment Marked as Completed")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def payments(request):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    payments = base_models.Billing.objects.filter(patient=patient)
    context = {"payments": payments, "patient": patient}
    return render(request, "patient/payments.html", context)


@login_required
def notifications(request):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    notifications = patient_models.Notification.objects.filter(patient=patient)
    notifications.update(seen=True)
    context = {"notifications": notifications, "patient": patient}
    return render(request, "patient/notifications.html", context)


@login_required
def mark_noti_seen(request, id):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    notification = patient_models.Notification.objects.get(id=id, patient=patient)
    notification.seen = True
    notification.save()
    return redirect("patient:notifications")


@login_required
def profile(request):
    patient, created = patient_models.Patient.objects.get_or_create(user=request.user)
    if request.method == "POST":
        patient.full_name = request.POST.get("full_name", patient.full_name)
        patient.email = request.POST.get("email", patient.email)
        patient.mobile = request.POST.get("mobile", patient.mobile)
        patient.gender = request.POST.get("gender", patient.gender)
        patient.dob = request.POST.get("dob", patient.dob)
        patient.blood_group = request.POST.get("blood_group", patient.blood_group)
        patient.address = request.POST.get("address", patient.address)
        if request.FILES.get("image"):
            patient.image = request.FILES["image"]
        patient.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect("patient:profile")
    context = {"patient": patient}
    return render(request, "patient/profile.html", context)
