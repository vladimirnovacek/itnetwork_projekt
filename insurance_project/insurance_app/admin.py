"""
Settings of the admin page
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from . import models


class OptionalLastNameUserCreationForm(UserCreationForm):
    last_name = forms.CharField(required=False, label='Příjmení')


class OptionalLastNameUserChangeForm(UserChangeForm):
    last_name = forms.CharField(required=False, label='Příjmení')


class PersonAdmin(UserAdmin):
    """
    Encapsulate all admin options and functionality for a given model.
    """
    form = OptionalLastNameUserChangeForm
    add_form = OptionalLastNameUserCreationForm
    list_display: tuple = ('email', 'date_of_birth', 'is_superuser')
    list_filter: tuple = ('is_superuser', 'is_staff')
    fieldsets: tuple = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    ordering = ('email',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Contract)
admin.site.register(models.Product)
admin.site.unregister(Group)
