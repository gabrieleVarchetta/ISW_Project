from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    category = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Product: {self.name}, Price: {self.price}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Order(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


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


class ResidentialAddress(Address):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
