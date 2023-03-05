
from django.urls import path

from . import views

urlpatterns = [
    path("seznam-klientu/", views.ClientListView.as_view(), name="clients-list"),
    # path('produkty', views.ProductsListView.as_view(), 'products-list')
]
