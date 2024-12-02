# Register your models here.
from django.contrib import admin
from .models import  Sale, Customer


admin.site.register(Sale)
admin.site.register(Customer)
