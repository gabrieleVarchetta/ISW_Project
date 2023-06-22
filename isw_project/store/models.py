from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import Lower

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    category = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Product: {self.name}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class PaymentMethod(models.Model):
    card_number = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    cardholder_name = models.CharField(max_length=100)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.CharField(max_length=4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    default_payment_method = models.BooleanField(default=False)

    def __str__(self):
        return f'{"*"*12}{self.card_number[12:]}'


class Order(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)

    def get_cart_products(self):
        return self.products.all()

    def get_cart_total(self):
        return sum([cart_product.product.price * cart_product.quantity for cart_product in self.products.all()])


class Address(models.Model):
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    street_address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=256)
    province = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.postal_code}, {self.region}, {self.country}'

    class Meta:
        abstract = True


class ShippingAddress(Address):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    default_shipping_address = models.BooleanField(default=False)


class ResidentialAddress(Address):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class ProductSales(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    product_total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_total_unit = models.PositiveIntegerField(default=0)

    def get_product_name(self):
        return self.product.name

    def get_product_price(self):
        return self.product.name

    def get_product_category(self):
        return self.product.category
