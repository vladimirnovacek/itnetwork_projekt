"""
Url patterns for the administration app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("seznam-klientu/", views.ClientListView.as_view(), name="clients-list"),
    path('odstanit-klienta/<int:pk>', views.delete_person, name='client-delete'),
    path('produkty/', views.ProductsListView.as_view(), name='products-list'),
    path('pridat-produkt/', views.ProductCreateView.as_view(), name='product-create'),
    path('produkt/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('odebrat-produkt/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('seznam-smluv/<int:pk>/', views.ContractsListView.as_view(), name='contracts-list'),
    path('nezpracovane-pojistne-udalosti/', views.PendingEventsListView.as_view(), name='pending-event-list'),
    path('udalost-<int:pk>/', views.EventDetailView.as_view(), name='event-detail')
]
