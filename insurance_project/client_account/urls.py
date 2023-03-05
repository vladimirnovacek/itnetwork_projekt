
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("smlouvy/", views.ContractsListView.as_view(), name="my-contracts"),
    path("zmena-udaju/", views.UpdateUserView.as_view(), name="person-update"),
    path("zmena-hesla/", views.PasswordChangeView.as_view(), name="password-change"),
    path("register-contract/", views.RegisterContractView.as_view(), name="register-contract"),
    path("<int:contract_number>/detail/", views.ContractDetailView.as_view(), name="contract-detail"),
    path("<int:contract_number>/upravit/", views.UpdateContractView.as_view(), name="contract-update"),
]
