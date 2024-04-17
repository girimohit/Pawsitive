from django.shortcuts import render, redirect
from django.http import HttpResponse
from baseapp.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, "index.html")


def check_pet_health(request):
    return render(request, "pet_health_check.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        location = request.POST.get("location")

        # Create new CustomUser instance
        new_user = User(
            username=username,
            email=email,
            dob=dob,
            location=location,
        )
        new_user.set_password(
            password
        )  # Manually set the password (don't forget this step)
        new_user.save()

        # Log the user in
        login(request, new_user)

        # Redirect to some success page
        return redirect("baseapp:HomePage")

    return render(request, "auth/register.html")


def login_user(request):
    if request.method == "POST":
        # Extract username and password from the form
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Authenticate userF
        user = authenticate(request, username=username, password=password)

        # Check if user authentication is successful
        if user is not None:
            # Log the user in
            login(request, user)

            # Redirect to some success page
            return redirect("baseapp:HomePage")
        else:
            # Authentication failed, handle this error accordingly
            return render(request, "auth/login.html", {"error": "Invalid credentials"})

    return render(request, "auth/login.html")
