import datetime
from django.test import TestCase
from . import models
from django.contrib.auth.models import User


class CustomerModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg')
        models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))

    def test_string_method(self):
        customer = models.Customer.objects.get(id=1)
        expected_res = f'{customer.user.first_name} {customer.user.first_name}'
        self.assertEqual(str(customer), expected_res)

    def test_create(self):
        self.assertEqual(len(models.Customer.objects.all()), 2)


class ProductModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Product.objects.create(name='iPhone 14', description='blablabla', category='Smartphone',
                                      price=899.99)

    def test_string_method(self):
        product = models.Product.objects.get(id=1)
        expected_res = product.name
        self.assertEqual(str(product), expected_res)

    def test_create(self):
        self.assertEqual(len(models.Product.objects.all()), 1)
