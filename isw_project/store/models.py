from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    category = models.CharField(max_length=256)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    price = models.FloatField()
    placed_at = models.DateTimeField(auto_now_add=True)


class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartProduct(models.Model):
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class OrderProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Address(models.Model):
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    street_address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=256)
    province = models.CharField(max_length=256)

    class Meta:
        abstract = True


class ShippingAddress(Address):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class ResidentialAddress(Address):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
