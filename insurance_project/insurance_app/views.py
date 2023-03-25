"""
Views for the insurance_app
"""
from django.contrib import messages
from django.contrib.auth import login, get_user_model, views as auth_views
from django.contrib.auth.base_user import AbstractBaseUser
from django.forms import Form

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models
from insurance_project import template_names as template


class IndexView(generic.ListView):
    """
    View for the index page
    """
    model:models.Product = models.Product
    template_name: str = template.HOME

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Processes the GET requests
        :param HttpRequest request:
        :param args:
        :param kwargs:
        :return HttpResponse:
        """
        object_list = self.get_queryset()
        active = object_list.filter(active=True)
        inactive = object_list.filter(active=False)
        return render(request, self.template_name, {"active": active, "inactive": inactive})


class RegisterUserView(generic.CreateView):
    """
    View displaying the client registration form
    """
    model: AbstractBaseUser = get_user_model()
    form_class: Form = forms.RegisterPersonForm
    template_name: str = template.FORM
    title: str = 'Registrace'
    success_url = reverse_lazy('register-contract')

    def get_context_data(self, **kwargs) -> dict:
        """
        Returns the default context data with additional 'title' variable
        :param kwargs:
        :return dict:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle POST requests. If form is valid, creates the new user and logs them in.
        :param HttpRequest request:
        :param args:
        :param kwargs:
        :return HttpResponse:
        """
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            messages.success(
                request,
                'Váš účet byl úspěšně vytvořen. Nyní si můžete uzavřít svou první smlouvu u naší společnosti'
            )
            login(request, self.object)
            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {"form": form, 'title': self.title})


class AboutView(generic.TemplateView):
    """
    View displaying a static 'About us' page
    """
    template_name = template.ABOUT


class LoginView(auth_views.LoginView):
    """
    The default django login view is used, this class only sets a page where the client is redirected after login
    """
    next_page = "my-contracts"
