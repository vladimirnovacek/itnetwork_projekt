from django.contrib import messages
from django.contrib.auth import views as auth_views, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import RestrictedError
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from client_account import forms
from insurance_app import models
from insurance_project import template_names as template


class ContractsListView(LoginRequiredMixin, generic.ListView):
    # TODO odstranit LoginRequiredMixin, asi neni potřeba. Asi...
    model = models.Contract
    template_name = template.CONTRACTS
    title = "Moje smlouvy"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(insured=self.request.user)
        return queryset


class RegisterContractView(generic.CreateView):
    form_class = forms.RegisterContractForm
    template_name = template.FORM
    title = 'Uzavřít smlouvu'
    success_url = reverse_lazy("my-contracts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
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


class ContractDetailView(generic.DetailView):
    model = models.Contract
    template_name = template.CONTRACT_DETAIL
    # title = None  # Title is the name of the contract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product.name
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        contract_number = kwargs.get('contract_number')
        if "edit" in request.POST:
            return redirect("contract-update", contract_number)
        if "delete" in request.POST:
            self.__delete_object()
            return redirect("my-contracts")

    def get_queryset(self):
        queryset = super().get_queryset()
        self.kwargs['pk'] = self.model.get_pk_by_contract_number(self.kwargs.get('contract_number'))
        return queryset

    def __delete_object(self):
        if not self.object:
            messages.warning(self.request, 'Smlouvu se nepodařilo zrušit')
            return
        messages.success(self.request, 'Smlouva byla úspěšně zrušena')
        self.object.delete()


class UpdateContractView(generic.UpdateView):
    form_class = forms.UpdateContractForm
    template_name = template.FORM
    model = models.Contract
    title = 'Upravit {} číslo {}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.format(self.object.product.name, self.object.contract_number)
        return context

    def get_success_url(self):
        return reverse("my-contracts")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Detaily smlouvy byly upraveny')
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        self.kwargs['pk'] = self.model.get_pk_by_contract_number(self.kwargs.get('contract_number'))
        return queryset


class LoginView(auth_views.LoginView):
    next_page = "my-contracts"


class UpdateUserView(generic.UpdateView):
    form_class = forms.UpdateUserForm
    template_name = template.FORM
    model = form_class.Meta.model
    title = 'Nastavení osobních údajů'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(pk=self.request.user.pk)
        return queryset.get()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaše údaje byly úspěšně změněny')
            return redirect("my-contracts")


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = template.FORM
    success_url = reverse_lazy('my-contracts')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Heslo bylo úspěšně změněno')
        return response


def delete_person(request):
    person = request.user
    try:
        person.delete()
    except RestrictedError:
        messages.error(
            request,
            "Nemůžeme uzavřít Váš účet, dokud u nás máte uzavřenou nějakou smlouvu."
            " Nejprve ukončete všechny své platné smlouvy."
        )
        return redirect(request.META['HTTP_REFERER'])
    else:
        auth_logout(request)
        return redirect('home')


def logout(request):
    auth_logout(request)
    messages.info('Byli jste odhlášeni')
    return redirect('home')
