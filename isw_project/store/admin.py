from django.contrib import admin
from django.db.models.functions import Lower

from .models import Customer, Product, Order


# Register your models here.


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_filter = ["category"]
    search_fields = ["name"]

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ["price", "placed_at", "customer"]
    



