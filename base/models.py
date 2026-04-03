from django.db import models
from shortuuid.django_fields import ShortUUIDField
from doctor import models as doctor_models
from patient import models as patient_models


class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,
                               help_text="Cost in Indian Rupees (₹)")
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.cost}"


class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='service_appointments')
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='doctor_appointments')
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='appointments_patient')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS, default="Pending")

    def __str__(self):
        return f"{self.patient.full_name} with Dr. {self.doctor.full_name}"


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"Medical Record for {self.appointment.patient.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.test_name}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"


class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='billings')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                    related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2,
                                    help_text="Amount in INR")
    tax = models.DecimalField(max_digits=10, decimal_places=2,
                              help_text="GST 5% in INR")
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text="Total in INR")
    status = models.CharField(max_length=120, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')],
                              default='Unpaid')
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    utr_number = models.CharField(max_length=50, null=True, blank=True,
                                  help_text="UPI Transaction Reference Number")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for {self.patient.full_name} - ₹{self.total}"
