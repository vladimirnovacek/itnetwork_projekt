from django.contrib import admin
from django.contrib.auth.models import User, Group

from . import models

admin.register(User, Group)
admin.site.register(models.Person)
admin.site.register(models.Insurance)
admin.site.register(models.Product)
