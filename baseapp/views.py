from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import connection
from baseapp.models import User, Pets, Adoption_Requests


def home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        location = request.POST.get("location")
        new_user = User(
            username=username,
            email=email,
            dob=dob,
            location=location,
        )
        new_user.set_password(password)
        new_user.save()
        login(request, new_user)
        return redirect("baseapp:HomePage")
    return render(request, "auth/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("baseapp:HomePage")
        else:
            return render(request, "auth/login.html", {"error": "Invalid credentials"})
    return render(request, "auth/login.html")


def logout_user(request):
    logout(request)
    return redirect("baseapp:HomePage")


def check_pet_health(request):
    if request.method == "POST":
        log_id = request.POST.get("logID")
        pet_id = request.POST.get("petID")
        pet_name = request.POST.get("petName")
        pet = Pets.objects.get(PetID=pet_id)

        print(pet.Health_Status)
        return render(request, "pet_health_check.html", {"pet": pet})
    return render(request, "pet_health_check.html")


def pet_adoption_status(request):
    if request.method == "POST":
        req_id = request.POST.get("request_id")
        pet_id = request.POST.get("pet_id")
        requester_id = request.POST.get("requester_id")
        req_date = request.POST.get("request_date")
        adoption_status = Adoption_Requests.objects.get(RequestID=req_id)
        print(adoption_status)
        print(adoption_status.Approval_Status)
        return render(
            request, "adoption_status.html", {"adoption_status": adoption_status}
        )
    return render(request, "adoption_status.html")




def query_test(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Pet_Name, Species, Health_Status FROM baseapp_pets WHERE Health_Status <> 'Healthy'")
        res_rows = cursor.fetchall()
        for i in res_rows:
            print(i)
    return render(request, "querytest.html")
