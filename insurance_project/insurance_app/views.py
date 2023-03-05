from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from . import forms, models
from insurance_project import template_names as template


class IndexView(generic.ListView):
    model = models.Product
    template_name = template.HOME

    def get(self, request, *args, **kwargs):
        object_list = self.get_queryset()
        active = object_list.filter(active=True)
        inactive = object_list.filter(active=False)
        return render(request, self.template_name, {"active": active, "inactive": inactive})


class RegisterUserView(generic.CreateView):
    form_class = forms.RegisterPersonForm
    template_name = template.FORM
    title = 'Registrace'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': self.title})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect(self.get_success_url())
        return render(request, self.template_name, {"form": form, 'title': self.title})

    def get_success_url(self):
        return reverse("register-contract")
