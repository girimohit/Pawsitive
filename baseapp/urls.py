from django.urls import path, include
from baseapp import views

app_name = "baseapp"

urlpatterns = [
    path("", views.home, name="HomePage"),
]
