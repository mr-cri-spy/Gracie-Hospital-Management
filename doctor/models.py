from django.db import models
from django.utils import timezone
from userauths import models as userauths_models

NOTIFICATION_TYPE = (
    ("New Appointment", "New Appointment"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


class Doctor(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to="images", null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True,
                              help_text="Indian mobile number e.g. 98765 43210")
    city = models.CharField(max_length=100, default="Mysore", null=True, blank=True)
    state = models.CharField(max_length=100, default="Karnataka", null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualifications = models.CharField(max_length=200, null=True, blank=True)
    years_of_experience = models.CharField(max_length=10, null=True, blank=True)
    registration_number = models.CharField(max_length=50, null=True, blank=True,
                                           help_text="Karnataka Medical Council Reg. No.")
    next_available_appointment_date = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.full_name}"

    class Meta:
        verbose_name = "Doctor"


class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name="doctor_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"Dr {self.doctor.full_name} Notification"
