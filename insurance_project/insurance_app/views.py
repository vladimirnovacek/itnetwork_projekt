from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from . import forms, models

HOME_TEMPLATE = "insurance_app/home.html"
FORM_TEMPLATE = "insurance_app/dummy_form_template.html"
CONTRACTS_TEMPLATE = "insurance_app/my_contracts.html"
CONTRACT_DETAIL_TEMPLATE = "insurance_app/contract_detail.html"


class IndexView(generic.ListView):
    model = models.Product
    template_name = HOME_TEMPLATE

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        active = self.object_list.filter(active=True)
        inactive = self.object_list.filter(active=False)
        return render(request, self.template_name, {"active": active, "inactive": inactive})


class RegisterUserView(generic.CreateView):
    form_class = forms.RegisterUserForm
    template_name = FORM_TEMPLATE

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect(self.get_success_url())
        return render(request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse("register-detail")


class RegisterUserDetailView(generic.CreateView):
    form_class = forms.RegisterUserDetailsForm
    template_name = FORM_TEMPLATE

    @login_required
    def get(self, request, *args, **kwargs):
        return super(RegisterUserDetailView, self).get(request, *args, **kwargs)

    @login_required
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass
        if hasattr(request, "user"):
            person = form.save(commit=False)
            person.user = request.user
            person.save()
        return self.get_success_url()

    def get_success_url(self):
        return reverse("register-contract")


class UpdateUserView(generic.UpdateView):
    form_class = FORM_TEMPLATE

class LoginView(auth_views.LoginView):
    next_page = "my-contracts"


class RegisterContractView(generic.CreateView):
    form_class = forms.RegisterInsurance
    template_name = FORM_TEMPLATE

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if hasattr(request, "user"):
            contract = form.save(commit=False)
            contract.insured = request.user
            contract.save()
        return self.get_success_url()

    def get_success_url(self):
        return reverse("my-contracts")


class UpdateContractView(generic.UpdateView):
    form_class = forms.UpdateInsurance
    template_name = FORM_TEMPLATE
    model = models.Contract

    def get_success_url(self):
        return reverse("my-contracts")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        contract_number = self.kwargs.get("contract_number")
        pk = self.model.get_pk_by_contract_number(contract_number)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class ContractsView(LoginRequiredMixin, generic.ListView):
    model = models.Contract
    template_name = CONTRACTS_TEMPLATE

    def get(self, request, *args, **kwargs):
        user = request.user
        object_list = self.model.objects.filter(insured=user)
        return render(request, self.template_name, {"object_list": object_list})


class ContractDetailView(generic.DetailView):
    model = models.Contract
    template_name = CONTRACT_DETAIL_TEMPLATE

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, self.template_name, {"obj": self.object})

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        if "edit" in request.POST:
            return redirect("contract-update", self.object.contract_number)
        if "delete" in request.POST:
            self.__delete_object()
            return redirect("my-contracts")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        contract_number = self.kwargs.get("contract_number")
        pk = self.model.get_pk_by_contract_number(contract_number)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def __delete_object(self):
        if not self.object:
            return
        self.object.delete()
