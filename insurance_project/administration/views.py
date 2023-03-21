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
    View displaying products list.
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
        Extends the parent method with additional context of the page title.
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
    paginate_by = 10
    # queryset: QuerySet = models.Person.objects.filter(is_staff=False).order_by('last_name', 'first_name')
    template_name: str = template.CLIENT_LIST
    title: str = "Seznam klientů"

    def get_queryset(self):
        queryset = models.Person.objects.filter(is_staff=False).order_by('last_name', 'first_name')
        if 'name-search' in self.request.POST:
            queryset = queryset.filter(last_name__contains=self.request.POST['name-search'])
        return queryset

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
        page = self.request.GET.get('page', 1)
        context['page_range'] = self.get_paginator(self.get_queryset(), self.paginate_by)\
            .get_elided_page_range(page, on_each_side=2)
        if 'name-search' in self.request.POST:
            context['name_search'] = self.request.POST['name-search']
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
        context['pk'] = self.person.pk
        context['title'] = self.title.format(self.person)
        return context

    def get_queryset(self) -> QuerySet:
        """
        Filter default queryset by client's primary key
        :return QuerySet:
        """
        self.person = models.Person.objects.get(pk=self.kwargs['pk'])
        queryset = super().get_queryset()
        queryset = queryset.filter(insured=self.person)
        return queryset


class PendingEventsListView(generic.ListView):
    """
    View for displaying all unprocessed insured events
    """
    model: models.InsuredEvent = models.InsuredEvent
    template_name: str = template.PENDING_EVENT_LIST
    title: str = "Nezpracované pojistné události"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        return super().get_queryset().filter(processed=False).order_by('-reporting_date')


class EventDetailView(generic.UpdateView):
    model = models.InsuredEvent
    template_name = template.EVENT_DETAIL
    title = "Škodní událost č. {}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.format(self.get_object().pk)
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object: models.InsuredEvent = self.get_object()
        if 'approve' in request.POST:
            if not 'payout' in request.POST or not request.POST['payout']:
                pass
        elif 'reject' in request.POST:
            self.object.approved = False
        else:
            return self.get(request, *args, **kwargs)


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
    return redirect('clients-list')
