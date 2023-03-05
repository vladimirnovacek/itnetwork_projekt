
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("moje/", include("django.contrib.auth.urls")),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    # path('sprava/produkty', views.ProductsListView.as_view(), 'products-list')
]
