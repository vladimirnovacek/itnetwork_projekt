from django.contrib import messages
from django.db.models import RestrictedError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from administration import forms
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


class ProductCreateView(generic.CreateView):
    form_class = forms.ProductCreateForm
    model = models.Product
    template_name = template.FORM
    title = 'Nový produkt'

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data(title=self.title))

    def get_success_url(self):
        return reverse('products-list')


class ProductUpdateView(generic.UpdateView):
    form_class = forms.ProductUpdateForm
    model = models.Product
    template_name = template.FORM

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(title=self.object.name))

    def get_success_url(self):
        return reverse('products-list')


class ProductDeleteView(generic.UpdateView):
    model = models.Product

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active = False
        self.object.save()
        return redirect('products-list')


class ClientListView(generic.ListView):
    model = models.Person
    queryset = models.Person.objects.filter(is_staff=False)
    template_name = template.CLIENT_LIST
    title = "Seznam klientů"

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            request.title = self.title
            return super().get(request, *args, **kwargs)


class ContractsList(generic.ListView):
    model = models.Contract
    template_name = template.ADMIN_CONTRACTS_LIST

    def get(self, request, *args, **kwargs):
        self.person = models.Person.objects.get(pk=kwargs['pk'])
        title = f'Smlouvy klienta {self.person}'
        self.queryset = self.get_queryset().filter(insured=self.person)
        return render(request, self.template_name, {'objects_list': self.queryset, 'title': title})


def delete_person(request, pk):
    person = get_object_or_404(models.Person, pk=pk)
    try:
        person.delete()
    except RestrictedError:
        messages.error(
            request,
            "Nelze smazat klienta, který má uzavřené smlouvy. Ukončete nejprve všechny jeho smlouvy."
        )
    return redirect(request.META['HTTP_REFERER'])

