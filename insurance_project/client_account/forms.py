"""
Module containing form classes of the client_account app
"""
from django import forms
from django.db.models import Model

from insurance_app import models


class RegisterContractForm(forms.ModelForm):
    """
    Form for creating new contracts
    """
    model: Model = models.Contract
    product: forms.Field = forms.ModelChoiceField(queryset=models.Product.objects.filter(active=True), label='Produkt')

    class Meta:
        model = models.Contract
        fields: list[str] = ["product", "payment"]


class UpdateContractForm(forms.ModelForm):
    """
    Form for updating contract details
    """
    class Meta:
        model: Model = models.Contract
        fields: list[str] = ["payment"]


class CreateInsuredEvent(forms.ModelForm):
    """
    Form for creating a new insured event
    """
    class Meta:
        model: Model = models.InsuredEvent
        fields: list[str] = ['event_date', 'description']


class UpdateUserForm(forms.ModelForm):
    """
    Form for updating client's personal informations
    """
    class Meta:
        model: Model = models.Person
        fields: list[str] = ["phone", "address1", "address2", "postal_code", "city", "country"]
