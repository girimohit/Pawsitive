from django.urls import path, include
from baseapp import views

app_name = "baseapp"

urlpatterns = [
    path("", views.home, name="HomePage"),
    path("check-pet-health", views.check_pet_health, name="get_pet_health"),
    path("register", views.register, name="register_user"),
    path("login", views.login_user, name="login_user"),
]
