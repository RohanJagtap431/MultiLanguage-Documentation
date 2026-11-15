
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
)

User = get_user_model()


def landing_view(request):

    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("/admin/")

        return redirect("documentation_home")

    return redirect("register")

def register_view(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        mobile_number = request.POST.get("mobile_number", "").strip()

        if not name or not mobile_number:
            messages.error(request, "All fields are required.")

        elif not mobile_number.isdigit() or not (10 <= len(mobile_number) <= 15):
            messages.error(request, "Enter a valid mobile number.")

        elif User.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, "This mobile number is already registered.")

        else:
            User.objects.create_user(
                name=name,
                mobile_number=mobile_number,
                is_active=False,
                is_approved=False,
            )

            messages.success(
                request,
                "Registration successful! Wait for admin approval."
            )

            return redirect("register")

    return render(request, "accounts/register.html")


def login_view(request):

    if request.method == "POST":

        mobile_number = request.POST.get("mobile_number", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            mobile_number=mobile_number,
            password=password,
        )

        if user is not None:

            if user.is_superuser:
                login(request, user)
                return redirect("/admin/")

            if user.is_approved and user.is_active:
                login(request, user)
                return redirect("documentation_home")

            messages.error(
                request,
                "Your account is waiting for admin approval."
            )

        else:
            messages.error(
                request,
                "Invalid mobile number or password."
            )

    return render(request, "accounts/login.html")

def logout_view(request):

    logout(request)
    return redirect("login")
