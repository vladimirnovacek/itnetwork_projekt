"""
Url patterns for the insurance_app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path('about/', views.AboutView.as_view(), name='about')
]
