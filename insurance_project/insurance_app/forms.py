"""
Module containing form classes of the insurance_app
"""
from typing import Any

from django.contrib.auth.forms import UserCreationForm
from django.forms import DateField

from . import models


class RegisterPersonForm(UserCreationForm):
    """
    Form for creating a new person object
    """
    date_of_birth = DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = models.Person
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'phone', 'address1',
                  'address2', 'city', 'postal_code', 'country']

    def save(self, commit=True) -> Any:
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
