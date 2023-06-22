from django.contrib import admin
from .models import Product as ProductModel, ProductSales as ProductSalesModel, OrderProduct as OrderProductModel


# Register your models here.
@admin.register(ProductModel)
class Product(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(ProductSalesModel)
class ProductSales(admin.ModelAdmin):
    list_display = ['get_product_name', 'get_product_price', 'get_product_category', 'product_total_sales', 'product_total_unit']
    list_filter = ["product__category"]
    search_fields = ["product__name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        products = ProductModel.objects.all()

        queryset = list(queryset)
        for product in products:
            order_products = OrderProductModel.objects.filter(order__pending=False, product=product)
            total_units_sold = sum([product.quantity for product in order_products])
            total_sales = product.price * total_units_sold
            product_sales, _ = ProductSalesModel.objects.get_or_create(product=product)
            product_sales.product_total_sales = total_sales
            product_sales.product_total_unit = total_units_sold
            product_sales.save()
            queryset.append(product_sales)

        updated_queryset = ProductSalesModel.objects.filter(id__in=[product.id for product in queryset])
        return updated_queryset

    def has_add_permission(self, request):
        return False
