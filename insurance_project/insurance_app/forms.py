from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class RegisterPersonForm(UserCreationForm):

    class Meta:
        model = models.Person
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'phone', 'address1',
                  'address2', 'city', 'postal_code', 'country']
