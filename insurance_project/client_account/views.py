
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from client_account import forms
from insurance_app import models
from insurance_project import template_names as template


class ContractsView(LoginRequiredMixin, generic.ListView):
    model = models.Contract
    template_name = template.CONTRACTS

    def get(self, request, *args, **kwargs):
        user = request.user
        object_list = self.model.objects.filter(insured=user)
        return render(request, self.template_name, {"object_list": object_list})


class RegisterContractView(generic.CreateView):
    form_class = forms.RegisterContractForm
    template_name = template.FORM
    success_url = reverse_lazy("my-contracts")

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if hasattr(request, "user"):
            contract = form.save(commit=False)
            contract.insured = request.user
            contract.save()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ContractDetailView(generic.DetailView):
    model = models.Contract
    template_name = template.CONTRACT_DETAIL

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, self.template_name, {"obj": self.object})

    def post(self, request: HttpRequest):
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


class UpdateContractView(generic.UpdateView):
    form_class = forms.UpdateContractForm
    template_name = template.FORM
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


class LoginView(auth_views.LoginView):
    next_page = "my-contracts"


class UpdateUserView(generic.UpdateView):
    form_class = forms.UpdateUserForm
    template_name = template.FORM
    model = form_class.Meta.model

    def get(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(instance=self.model.objects.get(user=request.user))
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.model.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect("my-contracts")


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = template.FORM
