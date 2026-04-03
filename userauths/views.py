import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

from userauths import forms as userauths_forms
from doctor import models as doctor_models
from patient import models as patient_models
from userauths import models as userauths_models


def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.UserRegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")

            user = authenticate(request, email=email, password=password1)

            if user is not None:
                login(request, user)

                if user_type == "Doctor":
                    doctor_models.Doctor.objects.create(user=user, full_name=full_name)
                else:
                    patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)

                messages.success(request, "Account created successfully")
                return redirect("/")

            else:
                messages.error(request, "Authenticated failed, please try again!")

    else:
        form = userauths_forms.UserRegisterForm()

    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_instance = userauths_models.User.objects.get(email=email, is_active=True)
                user_authenticate = authenticate(request, email=email, password=password)

                if user_instance is not None:
                    login(request, user_authenticate)
                    messages.success(request, "Logged in successfully")
                    next_url = request.GET.get("next", '/')
                    return redirect(next_url)
                else:
                    messages.error(request, "Username or password does not exist!")
            except:
                messages.error(request, "User does not exist!")
    else:
        form = userauths_forms.LoginForm()
    
    context = {"form": form}
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("userauths:sign-in")


# ─── Forgot Password (OTP Flow) ──────────────────────────────────────────────

def forgot_password(request):
    """Step 1: User enters their email to receive OTP"""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = userauths_models.User.objects.get(email=email)
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            # Save OTP and email in session
            request.session["reset_otp"] = otp
            request.session["reset_email"] = email

            # Send OTP email
            send_mail(
                subject="Gracie Hospital — Password Reset OTP",
                message=f"Hi {user.username},\n\nYour OTP to reset your password is: {otp}\n\nThis OTP is valid for this session only. Do not share it with anyone.\n\n— Gracie Hospital, Mysore",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f"OTP sent to {email}. Please check your inbox.")
            return redirect("userauths:verify-otp")

        except userauths_models.User.DoesNotExist:
            messages.error(request, "No account found with this email address.")

    return render(request, "userauths/forgot_password.html")


def verify_otp(request):
    """Step 2: User enters the OTP received on email"""
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:
            messages.success(request, "OTP verified! Now set your new password.")
            return redirect("userauths:reset-password")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "userauths/verify_otp.html")


def reset_password(request):
    """Step 3: User sets a new password"""
    email = request.session.get("reset_email")
    if not email:
        messages.error(request, "Session expired. Please start again.")
        return redirect("userauths:forgot-password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Try again.")
        elif len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            try:
                user = userauths_models.User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                # Clear session
                del request.session["reset_otp"]
                del request.session["reset_email"]
                messages.success(request, "Password reset successful! Please login with your new password.")
                return redirect("userauths:sign-in")
            except userauths_models.User.DoesNotExist:
                messages.error(request, "Something went wrong. Please try again.")

    return render(request, "userauths/reset_password.html")
