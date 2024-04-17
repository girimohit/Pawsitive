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

question = ['''What is the average age of pets adopted by users from each location.''','''List pets which are no healthy.''','''Which are the top 3 most popular pet species based on adoption requests''','''Which are the top 3 most common species of pets in the database.''','''What is the total number of likes received on community posts made by users who have 
adopted pets of age less than 2 years.''',''' List the usernames of users who have made adoption requests for pets of the same breed 
as their own pets.''','''What is the total number of adoption requests made for each species of pets.''',''' What is the average change in happiness level of pets after each activity recorded in the pet 
care logs.''',''' Identify Pet Care Log info with the help of LogID and PetID''' ,'''What is the current approval status of adoption request''',''' What is the percentage of pets with a happiness level above 'Content' among all pets 
owned by users who have made adoption requests.''' ,''' Find the number of community posts made by users from each location, excluding users 
who have adopted pets older than 5 years.''',''' List the usernames of users who have made both adoption requests and community posts 
on the same day.''',''' .Find the average happiness change for each type of activity in Pet Care Logs''',''' What is the average number of comments received on community posts made by users 
who have adopted pets of different genders.''']


queryDbms = ['''SELECT u.Location, AVG(p.Age) AS Average_Age
 FROM Users u
 JOIN User_Pets up ON u.UserID = up.UserID
 JOIN Pets p ON up.PetID = p.PetID
 GROUP BY u.Location;''',''' SELECT Pet_Name, Species, Health_Status
 FROM Pets
 WHERE Health_Status <> 'Healthy'; ''',''' SELECT p.Species, COUNT(ar.RequestID) AS NumberOfRequests
 FROM Pets p
 JOIN Adoption_Requests ar ON p.PetID = ar.PetID
 GROUP BY p.Species
 ORDER BY NumberOfRequests DESC
 LIMIT 3; ''','''SELECT Species, COUNT(*) AS Total_Count
 FROM Pets
GROUP BY Species
 ORDER BY Total_Count DESC
 LIMIT 3; ''','''  SELECT SUM(cp.Likes) AS Total_Likes
 FROM Community_Posts cp
 JOIN Users u ON cp.AuthorID = u.UserID
 JOIN User_Pets up ON u.UserID = up.UserID
 JOIN Pets p ON up.PetID = p.PetID
 WHERE p.Age < 2;''',''' SELECT DISTINCT u.Username
 FROM Users u
 JOIN Adoption_Requests ar ON u.UserID = ar.RequesterID
 JOIN Pets p1 ON ar.PetID = p1.PetID
 JOIN User_Pets up ON u.UserID = up.UserID
 JOIN Pets p2 ON up.PetID = p2.PetID
 WHERE p1.Breed = p2.Breed;
''',''' SELECT p.Species, COUNT(*) AS Total_Adoption_Requests
 FROM Adoption_Requests ar
 JOIN Pets p ON ar.PetID = p.PetID
 GROUP BY p.Species; ''','''  SELECT Actviity_Type, AVG(Happiness_Change) AS Average_Happiness_Change
 FROM Pet_Care_Logs
 GROUP BY Actviity_Type;''','''SELECT *
 FROM Pet_Care_Logs
 WHERE LogID = 3 AND PetID = 3; ''','''SELECT 
ar.RequestID,
 ar.Approval_Status,
 u.Username AS Requester,
 p.Pet_Name AS Pet
 FROM Adoption_Requests ar
 JOIN Users u ON ar.RequesterID = u.UserID
 JOIN Pets p ON ar.PetID = p.PetID; ''',''' SELECT (COUNT(CASE WHEN p.Happiness_Level > 'Content' THEN 1 END) / COUNT(*)) * 100 
AS Percentage_Happy_Pets
 FROM Users u
 JOIN Adoption_Requests ar ON u.UserID = ar.RequesterID
 JOIN Pets p ON ar.PetID = p.PetID;''',''' SELECT u.Location, COUNT(cp.PostID) AS Num_Community_Posts
 FROM Users u
 LEFT JOIN Community_Posts cp ON u.UserID = cp.AuthorID
 JOIN User_Pets up ON u.UserID = up.UserID
 JOIN Pets p ON up.PetID = p.PetID
WHERE p.Age <= 5
 GROUP BY u.Location;''',''' SELECT DISTINCT u.Username
 FROM Users u
 JOIN Adoption_Requests ar ON u.UserID = ar.RequesterID
 JOIN Community_Posts cp ON u.UserID = cp.AuthorID
 WHERE DATE(ar.Request_Date) = DATE(cp.Post_Date); ''',''' SELECT Actviity_Type, AVG(Happiness_Change) AS AvgHappinessChange
 FROM Pet_Care_Logs
 GROUP BY Actviity_Type;''','''SELECT AVG(cp.Comments) AS Average_Comments
 FROM Users u
 JOIN Community_Posts cp ON u.UserID = cp.AuthorID
JOIN Adoption_Requests ar ON u.UserID = ar.RequesterID
 JOIN Pets p ON ar.PetID = p.PetID
 GROUP BY p.Gender;''']


def query_test(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Pet_Name, Species, Health_Status FROM baseapp_pets WHERE Health_Status <> 'Healthy'"
        )
        res_rows = cursor.fetchall()
        for i in res_rows:
            print(i)
    return render(request, "querytest.html")


def faq_page(request):
    return render(request, "faq.html")
