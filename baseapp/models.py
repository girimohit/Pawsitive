from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    dob = models.DateField()
    location = models.CharField(max_length=100)


class Pets(models.Model):
    PetID = models.AutoField(primary_key=True)
    Pet_Name = models.CharField(max_length=50)
    Species = models.CharField(max_length=50)
    Breed = models.CharField(max_length=50)
    Age = models.PositiveIntegerField()
    Gender = models.CharField(max_length=10)
    Health_Status = models.CharField(max_length=50, default="Healthy")
    Happiness_Level = models.CharField(max_length=50, default="Happy")
    Hunger_Level = models.CharField(max_length=50, default="Full")
    Hygiene_Level = models.CharField(max_length=50, default="clean")
    Exercise_Level = models.CharField(max_length=50, default="Active")
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Adoption_Requests(models.Model):
    RequestID = models.AutoField(primary_key=True)
    Pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    Requester = models.ForeignKey(User, on_delete=models.CASCADE)
    Request_Date = models.DateField()
    Approval_Status = models.CharField(max_length=10)


class Pet_Care_Logs(models.Model):
    LogID = models.AutoField(primary_key=True)
    Pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    Activity_Date = models.DateField()
    Actviity_Type = models.CharField(max_length=100)
    Happiness_Change = models.IntegerField()
    Hunger_Change = models.IntegerField()
    Hygiene_Change = models.IntegerField()
    Exercise_Change = models.IntegerField()


class Educational_Content(models.Model):
    ContentID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=50)
    Content_Description = models.CharField(max_length=50)
    Content_Type = models.CharField(max_length=50)
    Content = models.TextField()


class Community_Posts(models.Model):
    PostID = models.AutoField(primary_key=True)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Post_Date = models.DateField()
    Content = models.TextField()
    Likes = models.BigIntegerField()
    Comments = models.BigIntegerField()


class User_Pets(models.Model):
    UserPetID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    Adoption_Date = models.DateField()


class list_pets(models.Model):
    PetID = models.AutoField(primary_key=True)
    Pet_Name = models.CharField(max_length=50)
    Species = models.CharField(max_length=50)
    Breed = models.CharField(max_length=50)
    Age = models.PositiveIntegerField()
    Gender = models.CharField(max_length=10)
    Health_Status = models.CharField(max_length=50, default="Healthy")
    Happiness_Level = models.CharField(max_length=50, default="Happy")
    Hunger_Level = models.CharField(max_length=50, default="Full")
    Hygiene_Level = models.CharField(max_length=50, default="clean")
    Exercise_Level = models.CharField(max_length=50, default="Active")
    img_link = models.CharField(max_length=500)
