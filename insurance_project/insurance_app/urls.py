
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("moje/", include("django.contrib.auth.urls")),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("register-details/", views.RegisterUserDetailView.as_view(), name="register-detail"),
    path("register-contract/", views.RegisterContractView.as_view(), name="register-contract"),
    path("muj-ucet/login/", views.LoginView.as_view(), name="login"),
    path("muj-ucet/smlouvy/", views.ContractsView.as_view(), name="my-contracts"),
    path("muj-ucet/zmena-udaju/", views.UpdateUserView.as_view(), name="person-update"),
    path("muj-ucet/zmena-hesla/", views.PasswordChangeView.as_view(), name="password-change"),
    path("muj-ucet/<int:contract_number>/detail/", views.ContractDetailView.as_view(), name="contract-detail"),
    path("muj-ucet/<int:contract_number>/upravit/", views.UpdateContractView.as_view(), name="contract-update"),
    path("sprava/seznam-klientu/", views.ClientListView.as_view(), name="clients-list")
]
