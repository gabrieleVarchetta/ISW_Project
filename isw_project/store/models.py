from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    category = models.CharField(max_length=256)
    price = models.FloatField()
    # Altri campi del prodotto


class Order(models.Model):
    price = models.FloatField()
    placed_at = models.DateTimeField(auto_now_add=True)


class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='CartProduct')

    def add_product(self, product, quantity=1):
        cart_product, created = CartProduct.objects.get_or_create(cart=self, product=product)
        cart_product.quantity += quantity
        cart_product.save()

    def remove_product(self, product):
        CartProduct.objects.filter(cart=self, product=product).delete()

    def get_cart_items(self):
        return self.cart_product.all()


class CartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_product')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class OrderProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
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
