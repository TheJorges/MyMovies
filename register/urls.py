from django.urls import path
from . import views

urlpatterns = [
    path("", views.cinephile_register, name="register")
]
