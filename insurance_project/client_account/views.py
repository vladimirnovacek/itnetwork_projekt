"""
Views for the client_account app.
"""
from django.contrib import messages
from django.contrib.auth import views as auth_views, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.db.models import RestrictedError, Model, QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from client_account import forms
from insurance_app import models
from insurance_project import template_names as template


@method_decorator(login_required, name='get')
class ContractsListView(generic.ListView):
    """
    View for displaying client's contracts
    """
    model: Model = models.Contract
    template_name: str = template.CONTRACTS
    title: str = "Moje smlouvy"

    def get_context_data(self, *, object_list: QuerySet = None, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param QuerySet object_list:
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self) -> QuerySet:
        """
        Filter default queryset by logged in client
        :return QuerySet:
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(insured=self.request.user)
        return queryset


@method_decorator(login_required, name='get')
class RegisterContractView(generic.CreateView):
    """
    View for creating new contract to the client
    """
    form_class: Form = forms.RegisterContractForm
    template_name: str = template.FORM
    title: str = 'Uzavřít smlouvu'
    success_url = reverse_lazy("my-contracts")

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        form = self.form_class(request.POST)
        if hasattr(request, "user"):
            contract = form.save(commit=False)
            contract.insured = request.user
            contract.save()
        if form.is_valid():
            messages.success(request, 'Vaše smlouva byla úspěšně sjednána. Děkujeme Vám za Vaši důvěru')
            return self.form_valid(form)
        else:
            messages.warning(request, 'Formulář není vyplněný správně')
            return self.form_invalid(form)


@method_decorator(login_required, name='get')
class ContractDetailView(generic.DetailView):
    """
    View for displaying details of a given contract
    """
    model: models.Contract = models.Contract
    template_name: str = template.CONTRACT_DETAIL
    # title = None  # Title is the name of the contract

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product.name
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        contract_number = kwargs.get('contract_number')
        if "edit" in request.POST:
            return redirect("contract-update", contract_number)
        if "delete" in request.POST:
            if not hasattr(self, 'object'):
                self.object = self.get_object()
            self._delete_object()
            return redirect("my-contracts")

    def get_queryset(self) -> QuerySet:
        """
        The contract is identified by a contract number in the URL, not by pk. This method determines the pk and adds it
        to the self.kwargs attribute and returns a default queryset.
        :return QuerySet:
        """
        self.kwargs['pk'] = self.model.get_pk_by_contract_number(self.kwargs.get('contract_number'))
        return super().get_queryset()

    def _delete_object(self) -> None:
        """
        Delete a contract.
        :return None:
        """
        if not hasattr(self, 'object'):
            messages.warning(self.request, 'Smlouvu se nepodařilo zrušit')
            return
        messages.success(self.request, 'Smlouva byla úspěšně zrušena')
        self.object.delete()


@method_decorator(login_required, name='get')
class UpdateContractView(generic.UpdateView):
    """
    View for updating a contract
    """
    form_class: Form = forms.UpdateContractForm
    template_name: str = template.FORM
    model: models.Contract = models.Contract
    title: str = 'Upravit {} číslo {}'
    success_url = reverse_lazy('my-contracts')

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.format(self.object.product.name, self.object.contract_number)
        return context

    def form_valid(self, form: Form) -> HttpResponse:
        """
        Save the associated model and add a success message
        :param Form form: form to be validated
        :return HttpResponse:
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Detaily smlouvy byly upraveny')
        return response

    def get_queryset(self) -> QuerySet:
        """
        The contract is identified by a contract number in the URL, not by pk. This method determines the pk and adds it
        to the self.kwargs attribute and returns the default queryset.
        :return QuerySet:
        """
        queryset = super().get_queryset()
        self.kwargs['pk'] = self.model.get_pk_by_contract_number(self.kwargs.get('contract_number'))
        return queryset


@method_decorator(login_required, name='get')
class CreateInsuredEventView(generic.CreateView):
    """
    Create a new insured event
    """
    form_class: Form = forms.CreateInsuredEvent
    template_name: str = template.FORM
    title: str = 'Nahlášení pojistné události'
    success_url = reverse_lazy("my-contracts")

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Create new insured event with the corresponding contract
        :param HttpRequest request:
        :param args:
        :param kwargs:
        :return:
        :rtype HttpResponse:
        """
        contract = models.Contract.get_object_by_contract_number(self.kwargs['contract_number'])
        insured_event = models.InsuredEvent(contract=contract)
        form = self.form_class(request.POST, instance=insured_event)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='get')
class InsuredEventListView(generic.ListView):
    """
    View for displaying the list of the client's insured events
    """
    model = models.InsuredEvent
    template_name = template.EVENT_LIST
    title = 'Seznam pojistných událostí'

    def get_context_data(self, *, object_list: QuerySet = None, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return:
        :rtype: dict
        """
        if not object_list:
            object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['pending'] = object_list.filter(processed=False)
        context['processed'] = object_list.filter(processed=True)
        context['title'] = self.title
        return context

    def get_queryset(self) -> QuerySet:
        """
        Return client's events ordered by date in descending order
        :return:
        :rtype: QuerySet
        """
        queryset = super().get_queryset()
        return queryset.filter(contract__insured=self.request.user).order_by('reporting_date')


class LoginView(auth_views.LoginView):
    """
    The default django login view is used, this class only sets a page where the client is redirected after login
    """
    next_page = "my-contracts"


@method_decorator(login_required, name='get')
class UpdateUserView(generic.UpdateView):
    """
    View for updating client personal informations
    """
    form_class: forms.UpdateUserForm = forms.UpdateUserForm
    template_name: str = template.FORM
    model: Model = form_class.Meta.model
    title: str = 'Nastavení osobních údajů'

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.
        Extends the parent method with additional context of the page title.
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_object(self, queryset: QuerySet | None = None) -> Model:
        """
        Get a Person object of a loged in client
        :param QuerySet queryset:
        :return Model:
        """
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(pk=self.request.user.pk)
        return queryset.get()

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests
        :param HttpRequest request:
        :param list args:
        :param dict kwargs:
        :return HttpResponse:
        """
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaše údaje byly úspěšně změněny')
            return redirect("my-contracts")


@method_decorator(login_required, name='get')
class PasswordChangeView(auth_views.PasswordChangeView):
    """
    View for a password change
    """
    template_name: str = template.FORM
    success_url = reverse_lazy('my-contracts')

    def form_valid(self, form: Form) -> HttpResponse:
        """
        Adds a message about successfully changing the password
        :param Form form:
        :return HttpResponse:
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Heslo bylo úspěšně změněno')
        return response


@login_required
def delete_person(request: HttpRequest) -> HttpResponse:
    """
    View function for deleting a client's account
    :param HttpRequest request:
    :return HttpResponse:
    """
    person = request.user
    try:
        person.delete()
    except RestrictedError:
        messages.error(
            request,
            "Nemůžeme uzavřít Váš účet, dokud u nás máte uzavřenou nějakou smlouvu. "
            "Nejprve ukončete všechny své platné smlouvy."
        )
        return redirect(request.META['HTTP_REFERER'])
    else:
        auth_logout(request)
        messages.success(
            request,
            'Váš účet byl odstraněn. Pokud se někdy rozhodnete k nám vrátit, bude potřeba se zaregistrovat znovu.'
        )
        return redirect('home')


def logout(request: HttpRequest) -> HttpResponse:
    """
    View function for logging client out
    :param HttpRequest request:
    :return HttpResonse:
    """
    auth_logout(request)
    messages.info(request, 'Byli jste odhlášeni')
    return redirect('home')
