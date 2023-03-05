from django import forms

from insurance_app import models


class RegisterContractForm(forms.ModelForm):
    model = models.Contract
    product = forms.ModelChoiceField(queryset=models.Product.objects.filter(active=True))

    class Meta:
        model = models.Contract
        fields = ["product", "payment"]


class UpdateContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = ["payment"]


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = models.Person
        fields = ["phone", "address1", "address2", "postal_code", "city", "country"]
