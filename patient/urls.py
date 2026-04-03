from django.urls import path

from patient import views

app_name = "patient"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments", views.appointments, name="appointments"),
    path("appointments/<appointment_id>/", views.appointment_detail, name="appointment_detail"),

    path("cancel_appointment/<appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("activate_appointment/<appointment_id>/", views.activate_appointment, name="activate_appointment"),
    path("complete_appointment/<appointment_id>/", views.complete_appointment, name="complete_appointment"),

    path("payments/", views.payments, name="payments"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark_noti_seen/<id>/", views.mark_noti_seen, name="mark_noti_seen"),
    path("profile/", views.profile, name="profile"),
]