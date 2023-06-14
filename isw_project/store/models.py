from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
