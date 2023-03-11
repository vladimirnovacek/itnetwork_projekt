"""
Module containing form classes of the administration app
"""

from django import forms

from insurance_app import models


class ProductCreateForm(forms.ModelForm):
    """
    Form for creating new insurance product.
    """

    class Meta:
        model = models.Product
        fields = ['name', 'description', 'image']


class ProductUpdateForm(forms.ModelForm):
    """
    Form for updating an insurance product.
    """

    class Meta:
        model = models.Product
        fields = ['description', 'image']
