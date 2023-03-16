"""
Url patterns for the insurance_app.
"""
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("register/", views.RegisterUserView.as_view(), name="register"),
]
