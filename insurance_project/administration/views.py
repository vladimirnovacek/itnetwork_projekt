from django.http import Http404
from django.shortcuts import render
from django.views import generic

from insurance_app import models
from insurance_project import template_names as template


class ProductsListView(generic.ListView):
    model = models.Product
    template_name = template.PRODUCTS_LIST
    title = 'Seznam produktů'

    def get(self, request, *args, **kwargs):
        object_list = self.get_queryset()
        active = object_list.filter(active=True)
        inactive = object_list.filter(active=False)
        return render(request, self.template_name, {"active": active, "inactive": inactive, 'title': self.title})


class ClientListView(generic.ListView):
    model = models.Person
    template_name = template.CLIENT_LIST

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            return super().get(request, *args, **kwargs)
