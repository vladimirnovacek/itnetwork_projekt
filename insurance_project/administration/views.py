from django.contrib import messages
from django.db.models import RestrictedError
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = object_list if object_list else self.object_list
        active = queryset.filter(active=True)
        inactive = queryset.filter(active=False)
        context['active'] = active
        context['inactive'] = inactive
        context['title'] = self.title
        return context


class ProductCreateView(generic.CreateView):
    form_class = forms.ProductCreateForm
    model = models.Product
    template_name = template.PRODUCT_FORM
    title = 'Nový produkt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně vytvořen')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('products-list')


class ProductUpdateView(generic.UpdateView):
    form_class = forms.ProductUpdateForm
    model = models.Product
    template_name = template.PRODUCT_FORM
    # title = None  # title is the name of the product to be updated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně upraven')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('products-list')


class ProductDeleteView(generic.UpdateView):
    model = models.Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.active = False
        obj.save()
        return redirect('products-list')

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně odstraněn')
        return super().post(request, *args, **kwargs)


class ClientListView(generic.ListView):
    model = models.Person
    queryset = models.Person.objects.filter(is_staff=False)
    template_name = template.CLIENT_LIST
    title = "Seznam klientů"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ContractsListView(generic.ListView):
    model = models.Contract
    template_name = template.ADMIN_CONTRACTS_LIST
    title = 'Smlouvy klienta {}'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.format(models.Person.objects.get(pk=self.kwargs['pk']))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        person = models.Person.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(insured=person)
        return queryset


def delete_person(request, pk):
    person = get_object_or_404(models.Person, pk=pk)
    try:
        person.delete()
    except RestrictedError:
        messages.error(
            request,
            "Nelze smazat klienta, který má uzavřené smlouvy. Ukončete nejprve všechny jeho smlouvy."
        )
    else:
        messages.success(request, 'Klientský účet byl úspěšně odstraněn')
    return redirect(request.META['HTTP_REFERER'])
