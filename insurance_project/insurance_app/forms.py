from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class RegisterPersonForm(UserCreationForm):

    class Meta:
        model = models.Person
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'phone', 'address1',
                  'address2', 'city', 'postal_code', 'country']


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = models.Person
        fields = ["phone", "address1", "address2", "postal_code", "city", "country"]


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
