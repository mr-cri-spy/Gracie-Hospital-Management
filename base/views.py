from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import urllib.parse

from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models


def index(request):
    services = base_models.Service.objects.all()
    context = {"services": services}
    return render(request, "base/index.html", context)


def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, "base/service_detail.html", context)


@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.dob = dob
        patient.save()

        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
            status="Pending",
        )

        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = round(appointment.service.cost * 5 / 100, 2)
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()

        return redirect("base:checkout", billing.billing_id)

    context = {"service": service, "doctor": doctor, "patient": patient}
    return render(request, "base/book_appointment.html", context)


@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    # Build UPI payment URL for Google Pay
    upi_id = settings.GPAY_UPI_ID
    merchant_name = settings.GPAY_MERCHANT_NAME
    amount = billing.total
    txn_note = f"Appointment-{billing.billing_id}"

    upi_url = (
        f"upi://pay?pa={upi_id}"
        f"&pn={urllib.parse.quote(merchant_name)}"
        f"&am={amount}"
        f"&cu=INR"
        f"&tn={urllib.parse.quote(txn_note)}"
    )

    # Google Pay deep link (works on Android)
    gpay_url = (
        f"intent://pay?pa={upi_id}"
        f"&pn={urllib.parse.quote(merchant_name)}"
        f"&am={amount}"
        f"&cu=INR"
        f"&tn={urllib.parse.quote(txn_note)}"
        f"#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end"
    )

    context = {
        "billing": billing,
        "upi_id": upi_id,
        "upi_url": upi_url,
        "gpay_url": gpay_url,
        "merchant_name": merchant_name,
        "amount": amount,
        "txn_note": txn_note,
    }
    return render(request, "base/checkout.html", context)


@login_required
def upi_payment_confirm(request, billing_id):
    """Patient manually confirms payment after paying via UPI/GPay"""
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    if request.method == "POST":
        utr_number = request.POST.get("utr_number", "").strip()

        if utr_number:
            billing.status = "Paid"
            billing.utr_number = utr_number
            billing.save()

            billing.appointment.status = "Scheduled"
            billing.appointment.save()

            doctor_models.Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                type="New Appointment",
            )

            patient_models.Notification.objects.create(
                patient=billing.appointment.patient,
                appointment=billing.appointment,
                type="Appointment Scheduled",
            )

            # Send email notifications
            merge_data = {"billing": billing}
            try:
                subject = "New Appointment - Gracie Hospital"
                text_body = render_to_string("email/new_appointment.txt", merge_data)
                html_body = render_to_string("email/new_appointment.html", merge_data)
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.FROM_EMAIL,
                    to=[billing.appointment.doctor.user.email],
                    body=text_body,
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()

                subject = "Appointment Booked Successfully - Gracie Hospital"
                text_body = render_to_string("email/appointment_booked.txt", merge_data)
                html_body = render_to_string("email/appointment_booked.html", merge_data)
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.FROM_EMAIL,
                    to=[billing.appointment.patient.email],
                    body=text_body,
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()
            except Exception as e:
                print(f"Email error: {e}")

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        else:
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")

    return redirect("base:checkout", billing_id)


@login_required
def payment_status(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")
    context = {"billing": billing, "payment_status": payment_status}
    return render(request, "base/payment_status.html", context)
