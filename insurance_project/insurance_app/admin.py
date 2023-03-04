from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from . import models


class PersonAdmin(UserAdmin):
    list_display = ('email', 'date_of_birth', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    ordering = ('email',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Contract)
admin.site.register(models.Product)
admin.site.unregister(Group)
