from django.db import models

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


