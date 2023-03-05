
from django.urls import path

from . import views

urlpatterns = [
    path("seznam-klientu/", views.ClientListView.as_view(), name="clients-list"),
    path('produkty/', views.ProductsListView.as_view(), name='products-list'),
    path('pridat-produkt/', views.ProductCreateView.as_view(), name='product-create'),
    path('produkt/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update')
]
