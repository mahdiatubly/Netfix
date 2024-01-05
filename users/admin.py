from django.contrib import admin

from .models import Customer, Company

admin.site.register(Company)
admin.site.register(Customer)

