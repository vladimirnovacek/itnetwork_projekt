from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email"]


class RegisterUserDetailsForm(forms.ModelForm):

    class Meta:
        model = models.Person
        fields = ["address1", "address2", "postal_code", "city", "country", "phone"]


class RegisterInsurance(forms.ModelForm):
    model = models.Contract
    product = forms.ModelChoiceField(queryset=models.Product.objects.filter(active=True))

    class Meta:
        model = models.Contract
        fields = ["product", "payment"]


class UpdateInsurance(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = ["payment"]
