"""
Module containing form classes of the administration app
"""

from django import forms
from django.db.models import Model

from insurance_app import models


class ProductCreateForm(forms.ModelForm):
    """
    Form for creating new insurance product.
    """
    class Meta:
        model: Model = models.Product
        fields: forms.Field = ['name', 'description', 'image']


class ProductUpdateForm(forms.ModelForm):
    """
    Form for updating an insurance product.
    """
    class Meta:
        model: Model = models.Product
        fields: forms.Field = ['description', 'image']


class EventApproveForm(forms.ModelForm):
    """
    Form for approving insurance events.
    """
    approve = forms.ChoiceField(choices=((1, 'Schválit'), (0, 'Zamítnout')), widget=forms.RadioSelect(), label="")

    class Meta:
        model = models.InsuredEvent
        fields = ['payout']
