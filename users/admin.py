from django.contrib import admin

from .models import Customer, Company, UserBase

admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(UserBase)

