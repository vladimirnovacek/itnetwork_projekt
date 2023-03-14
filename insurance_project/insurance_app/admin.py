"""
Settings of the admin page
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from . import models


class PersonAdmin(UserAdmin):
    """
    Encapsulate all admin options and functionality for a given model.
    """
    list_display: tuple = ('email', 'date_of_birth', 'is_superuser')
    list_filter: tuple = ('is_superuser',)
    fieldsets: tuple = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    ordering = ('email',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Contract)
admin.site.register(models.Product)
admin.site.unregister(Group)
