
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("moje/", include("django.contrib.auth.urls")),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("register-details/", views.RegisterUserDetailView.as_view(), name="register-detail"),
    path("register-insurance/", views.RegisterInsuranceView.as_view(), name="register-insurance"),
    path("muj-ucet/login/", views.LoginView.as_view(), name="login"),
    path("muj-ucet/smlouvy/", views.ContractsView.as_view(), name="my_contracts"),
    path("muj-ucet/<int:contract_number>/detail/")
    # path("logout/", views.logout, name="logout")
]
