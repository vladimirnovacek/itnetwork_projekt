from django import forms

from insurance_app import models


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['description']
