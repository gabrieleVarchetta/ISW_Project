from django.contrib import admin
from .models import Product, ProductSales


# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(ProductSales)
class ProductSales(admin.ModelAdmin):
    list_display = ['get_product_name', 'get_product_price', 'get_product_category', 'product_total_sales', 'product_total_unit']
    list_filter = ["product__category"]
    search_fields = ["product__name"]
