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


class OrderModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        customer = models.Customer.objects.create(name='Francesco Congiu')
        models.Order.objects.create(price=17.17, customer=customer)

    def test_string_method(self):
        order = models.Order.objects.get(id=1)
        expected_res = f'Order {order.id}'
        self.assertEqual(str(order), expected_res)

    def test_default_pending_status(self):
        order = models.Order.objects.get(id=1)
        self.assertTrue(order.pending)

    def test_order_creation(self):
        self.assertEqual(len(models.Order.objects.all()), 1)


class OrderProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        customer = models.Customer.objects.create(name='Francesco Congiu')
        order = models.Order.objects.create(price=34.34, customer=customer)
        product = models.Product.objects.create(name='Mac Pro', price=17.17)
        models.OrderProduct.objects.create(order=order, product=product, quantity=2)

    def test_order_product_creation(self):
        order_product = models.OrderProduct.objects.get(id=1)
        self.assertEqual(order_product.quantity, 2)

    def test_order_product_relationships(self):
        order_product = models.OrderProduct.objects.get(id=1)
        self.assertEqual(order_product.order.price, 34.34)
        self.assertEqual(order_product.product.name, 'Mac Pro')

    def test_default_quantity(self):
        order_product = models.OrderProduct.objects.get(id=1)
        self.assertEqual(order_product.quantity, 1)

    def test_order_product_deletion(self):
        order_product = models.OrderProduct.objects.get(id=1)
        order_product.delete()
        self.assertEqual(len(models.OrderProduct.objects.all()), 0)


class CartProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = models.Product.objects.create(name='iPhone 14 PRO', price=2.99)
        models.CartProduct.objects.create(product=product, quantity=2)

    def test_cart_product_creation(self):
        cart_product = models.CartProduct.objects.get(id=1)
        self.assertEqual(cart_product.quantity, 2)

    def test_cart_product_relationships(self):
        cart_product = models.CartProduct.objects.get(id=1)
        self.assertEqual(cart_product.product.name, 'iPhone 14 PRO')

    def test_default_quantity(self):
        cart_product = models.CartProduct.objects.get(id=1)
        self.assertEqual(cart_product.quantity, 1)

    def test_cart_product_deletion(self):
        cart_product = models.CartProduct.objects.get(id=1)
        cart_product.delete()
        self.assertEqual(len(models.CartProduct.objects.all()), 0)


class ShoppingCartTest(TestCase):
    def setUp(self):
        self.customer = models.Customer.objects.create(name='Francesco Congiu')
        self.cart = models.ShoppingCart.objects.create(customer=self.customer)

        self.product1 = models.CartProduct.objects.create(name='iPad PRO', price=17.17)
        self.product2 = models.CartProduct.objects.create(name='Apple Watch ULTRA', price=20.20)

        self.cart.products.add(self.product1)
        self.cart.products.add(self.product2)

    def test_get_cart_products(self):
        cart_products = self.cart.get_cart_products()
        self.assertEqual(len(cart_products), 2)
        self.assertIn(self.product1, cart_products)
        self.assertIn(self.product2, cart_products)

    def test_get_cart_total(self):
        cart_total = self.cart.get_cart_total()
        expected_total = self.product1.price + self.product2.price
        self.assertEqual(cart_total, expected_total)


class AddressTest(TestCase):
    def setUp(self):
        self.customer = models.Customer.objects.create(name='Francesco Congiu')
        self.address_data = {
            'country': 'Italy',
            'region': 'Sardinia',
            'city': 'Domusnovas',
            'street_address': 'Via Fratelli Bandiera 17',
            'postal_code': '09015',
            'province': 'Sud Sardegna',
            'customer': self.customer,
        }

    def test_address_creation(self):
        address = models.ShippingAddress.objects.create(**self.address_data)
        self._assert_address_fields(address)

    def test_shipping_address_creation(self):
        shipping_address = models.ShippingAddress.objects.create(**self.address_data)
        self._assert_address_fields(shipping_address)
        self.assertEqual(shipping_address.customer, self.customer)

    def test_residential_address_creation(self):
        residential_address = models.ResidentialAddress.objects.create(**self.address_data)
        self._assert_address_fields(residential_address)
        self.assertEqual(residential_address.customer, self.customer)

    def _assert_address_fields(self, address):
        address = models.Address(**self.address_data)
        expected_string = f"{self.address_data['Italy']}, " \
                          f"{self.address_data['Sardinia']}, " \
                          f"{self.address_data['Domusnovas']}, " \
                          f"{self.address_data['Via Fratelli Bandiera 17']}, " \
                          f"{self.address_data['09015']}, " \
                          f"{self.address_data['Sud Sardegna']}"
        self.assertEqual(str(address), expected_string)
