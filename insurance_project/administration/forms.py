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


class EventApproveForm(forms.Form):
    payout = forms.CharField()

    def is_valid(self):
        pass


class EventApproveForm(forms.Form):
    payout = forms.CharField()

    def is_valid(self):
        pass
