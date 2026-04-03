from django.urls import path

from userauths import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),

    # Forgot Password OTP Flow
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("verify-otp/", views.verify_otp, name="verify-otp"),
    path("reset-password/", views.reset_password, name="reset-password"),
]