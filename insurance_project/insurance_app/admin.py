from django.contrib import admin
from django.contrib.auth.models import User, Group

from . import models

admin.register(models.Person)
admin.site.register(models.Person)
admin.site.register(models.Contract)
admin.site.register(models.Product)
