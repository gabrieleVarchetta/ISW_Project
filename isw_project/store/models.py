from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    id = models.AutoField()
    name = models.CharField()
    decription = models.TextField()
    category = models.CharField()
    price = models.FloatField()
    # Altri campi del prodotto
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField()
    date = models.DateTimeField()

class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')

class OrderProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    order = models.ManyToOneRel(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
class CartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()


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
