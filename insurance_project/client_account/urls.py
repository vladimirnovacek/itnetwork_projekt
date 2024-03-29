"""
Url patterns for the client_account app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path("smlouvy/", views.ContractsListView.as_view(), name="my-contracts"),
    path("zmena-udaju/", views.UpdateUserView.as_view(), name="person-update"),
    path('odstranit-ucet/', views.delete_person, name='account-delete'),
    path("zmena-hesla/", views.PasswordChangeView.as_view(), name="password-change"),
    path("register-contract/", views.RegisterContractView.as_view(), name="register-contract"),
    path("<int:contract_number>/detail/", views.ContractDetailView.as_view(), name="contract-detail"),
    path("<int:contract_number>/upravit/", views.UpdateContractView.as_view(), name="contract-update"),
    path("skodni-udalosti/", views.InsuredEventListView.as_view(), name='event-list'),
    path("<int:contract_number>/nova-udalost/", views.CreateInsuredEventView.as_view(), name='event-create')
]
