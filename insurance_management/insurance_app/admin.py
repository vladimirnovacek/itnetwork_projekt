from django.contrib import admin

from .models import Address, Insurance, Insured_event, Product, User

admin.site.register(Address)
admin.site.register(Insurance)
admin.site.register(Insured_event)
admin.site.register(Product)
admin.site.register(User)
