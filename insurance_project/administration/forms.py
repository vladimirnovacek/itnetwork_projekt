from django import forms

from insurance_app import models


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['name', 'description', 'image']


class ProductUpdateForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = models.Product
        fields = ['description', 'image']
