"""
Views for the administration app.
"""
from django.contrib import messages
from django.db.models import RestrictedError, QuerySet, Model
from django.forms import Form
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from administration import forms
from insurance_app import models
from insurance_project import template_names as template


class ProductsListView(generic.ListView):
    """
    View displaying products.
    """
    model: Model = models.Product
    template_name: str = template.PRODUCTS_LIST
    title: str = 'Seznam produktů'

    def get_context_data(self, *, object_list: QuerySet | None = None, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent's method with additional context of active and inactive products and the page title.
        :param QuerySet object_list: set of passed on objects
        :param dict kwargs: additional keyword arguments
        :return dict: context data
        """
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = object_list if object_list else self.object_list
        active = queryset.filter(active=True)
        inactive = queryset.filter(active=False)
        context['active'] = active
        context['inactive'] = inactive
        context['title'] = self.title
        return context


class ProductCreateView(generic.CreateView):
    """
    View for creating new products
    """
    form_class: Form = forms.ProductCreateForm
    model: Model = models.Product
    template_name: str = template.PRODUCT_FORM
    title: str = 'Nový produkt'
    success_url = reverse_lazy('products-list')

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of th page title.
        :param dict kwargs: additional keyword arguments
        :return dict: context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests.
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně vytvořen')
        return super().post(request, *args, **kwargs)


class ProductUpdateView(generic.UpdateView):
    """
    View for changing products
    """
    form_class: Form = forms.ProductUpdateForm
    model: Model = models.Product
    template_name: str = template.PRODUCT_FORM
    # title = None  # title is the name of the product to be updated
    success_url = reverse_lazy('products-list')

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param dict kwargs: additional keyword arguments
        :return dict: context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        print(type(reverse_lazy('products-list')))
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně upraven')
        return super().post(request, *args, **kwargs)


class ProductDeleteView(generic.UpdateView):
    """
    View for marking a product as inactive
    """
    model = models.Product

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        obj = self.get_object()
        obj.active = False
        obj.save()
        return redirect('products-list')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
                Handle POST requests
                :param HttpRequest request:
                :param list args:
                :param dict kwargs:
                :return HttpResponse:
                """
        if self.get_form().is_valid():
            messages.success(request, 'Produkt byl úspěšně odstraněn')
        return super().post(request, *args, **kwargs)


class ClientListView(generic.ListView):
    """
    View for displaying list of clients
    """
    model: Model = models.Person
    queryset: QuerySet = models.Person.objects.filter(is_staff=False)
    template_name: str = template.CLIENT_LIST
    title: str = "Seznam klientů"

    def get_context_data(self, *, object_list: QuerySet = None, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param QuerySet object_list:
        :param dict kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ContractsListView(generic.ListView):
    """
    View for displaying contracts of a client given by primary key in the URL
    """
    model: Model = models.Contract
    template_name: str = template.ADMIN_CONTRACTS_LIST
    title: str = 'Smlouvy klienta {}'

    def get_context_data(self, *, object_list: QuerySet = None, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param QuerySet object_list:
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.format(models.Person.objects.get(pk=self.kwargs['pk']))
        return context

    def get_queryset(self) -> QuerySet:
        """
        Filter default queryset by client's primary key
        :return QuerySet:
        """
        queryset = super().get_queryset()
        person = models.Person.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(insured=person)
        return queryset


def delete_person(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function for deleting a client account
    :param HttpRequest request:
    :param int pk: client's primary key
    :return HttpResponse:
    """
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
