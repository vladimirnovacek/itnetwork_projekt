from django import forms

from insurance_app import models


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['name', 'description']


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['description']
