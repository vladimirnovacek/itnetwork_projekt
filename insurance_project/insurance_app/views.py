from django.contrib import messages
from django.contrib.auth import login, get_user_model

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
    model = get_user_model()
    form_class = forms.RegisterPersonForm
    template_name = template.FORM
    title = 'Registrace'
    success_url = reverse_lazy('register-contract')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        # form = self.form_class(request.POST)
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
