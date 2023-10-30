from django.urls import path
from . import views

urlpatterns = [
    path("", views.cinephile_login, name="login"),
    path("logout", views.cinephile_logout,name="logout")
]
