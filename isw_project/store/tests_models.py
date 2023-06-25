import datetime
from django.test import TestCase
from . import models
from django.contrib.auth.models import User


class CustomerModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))

    def test_string_method(self):
        customer = models.Customer.objects.get(id=1)
        expected_res = f'{customer.user.first_name} {customer.user.last_name}'
        self.assertEqual(str(customer), expected_res)

    def test_create(self):
        self.assertEqual(len(models.Customer.objects.all()), 1)


class ProductModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Product.objects.create(name='iPhone 14', description='blablabla', category='Smartphone',
                                      price=899.99)

    def test_string_method(self):
        product = models.Product.objects.get(id=1)
        expected_res = f'Product: {product.name}, Price: {product.price}'
        self.assertEqual(str(product), expected_res)

    def test_create(self):
        self.assertEqual(len(models.Product.objects.all()), 1)


class OrderModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        customer = models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))
        models.Order.objects.create(customer=customer)

    def test_string_method(self):
        order = models.Order.objects.get(id=1)
        expected_res = f'Order {order.id}'
        self.assertEqual(str(order), expected_res)

    def test_order_creation(self):
        self.assertEqual(len(models.Order.objects.all()), 1)


class OrderProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        customer = models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))
        order = models.Order.objects.create(customer=customer, price=34.34)
        product = models.Product.objects.create(name='Mac Pro', price=17.17)
        models.OrderProduct.objects.create(order=order, product=product, quantity=2)

    def test_order_product_creation(self):
        order_product = models.OrderProduct.objects.get(id=1)
        self.assertEqual(order_product.quantity, 2)

    def test_order_product_relationships(self):
        order_product = models.OrderProduct.objects.get(id=1)
        self.assertEqual(float(order_product.order.price), 34.34)
        self.assertEqual(order_product.product.name, 'Mac Pro')

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

    def test_cart_product_deletion(self):
        cart_product = models.CartProduct.objects.get(id=1)
        cart_product.delete()
        self.assertEqual(len(models.CartProduct.objects.all()), 0)


class ShoppingCartTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        self.customer = models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 5, 11))
        self.cart = models.ShoppingCart.objects.create(customer=self.customer)
        prod1 = models.Product.objects.create(name='iPad PRO', price=17.17)
        prod2 = models.Product.objects.create(name='Apple Watch ULTRA', price=20.20)
        self.product1 = models.CartProduct.objects.create(product=prod1)
        self.product2 = models.CartProduct.objects.create(product=prod2)

        self.cart.products.add(self.product1)
        self.cart.products.add(self.product2)

    def test_get_cart_products(self):
        cart_products = self.cart.get_cart_products()
        self.assertEqual(len(cart_products), 2)
        self.assertIn(self.product1, cart_products)
        self.assertIn(self.product2, cart_products)

    def test_get_cart_total(self):
        cart_total = self.cart.get_cart_total()
        expected_total = self.product1.product.price * self.product1.quantity + self.product2.product.price * self.product2.quantity
        self.assertEqual(float(cart_total), round(expected_total, 2))


class AddressTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        self.customer = models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 5, 11))
        address_data = {
            'country': 'Italy',
            'region': 'Sardinia',
            'city': 'Domusnovas',
            'street_address': 'Via Fratelli Bandiera 17',
            'postal_code': '09015',
            'province': 'Sud Sardegna',
            'customer': self.customer,
        }
        self.shipping_address = models.ShippingAddress.objects.create(**address_data)
        self.residential_address = models.ResidentialAddress.objects.create(**address_data)

    def test_shipping_address_creation(self):
        shipping_address = models.ShippingAddress.objects.get(id=1)
        self.assertEqual(shipping_address.customer, self.customer)
        self.assertEqual(len(models.ShippingAddress.objects.all()), 1)

    def test_residential_address_creation(self):
        residential_address = models.ResidentialAddress.objects.get(id=1)
        self.assertEqual(residential_address.customer, self.customer)
        self.assertEqual(len(models.ResidentialAddress.objects.all()), 1)

    def test_shipping_address_string_method(self):
        shipping_address = models.ShippingAddress.objects.get(id=1)
        expected_res = f'{shipping_address.street_address}, {shipping_address.city}, {shipping_address.postal_code}, {shipping_address.region}, {shipping_address.country}'

        self.assertEqual(str(shipping_address), expected_res)

    def test_residential_address_string_method(self):
        residential_address = models.ResidentialAddress.objects.get(id=1)
        expected_res = f'{residential_address.street_address}, {residential_address.city}, {residential_address.postal_code}, {residential_address.region}, {residential_address.country}'

        self.assertEqual(str(residential_address), expected_res)


class PaymentMethodTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(first_name='Gabriele', last_name='Varchetta', email='gab@gmail.com',
                                        password='123456topg', username='gab')
        customer = models.Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))
        self.payment_method = models.PaymentMethod.objects.create(customer=customer, card_number='1234567890123456', cardholder_name='Gabriele Varchetta', expiration_year=25, expiration_month=6, cvv=1234)

    def test_payment_method_creation(self):
        self.assertEqual(len(models.PaymentMethod.objects.all()), 1)

    def test_string_method(self):
        expected_res = f'{"*"*12}3456'
        self.assertEqual(str(self.payment_method), expected_res)

    def test_relationship(self):
        expected_res = 'Gabriele Varchetta'
        self.assertEqual(str(self.payment_method.customer), expected_res)


class ProductSalesTest(TestCase):
    def setUp(self) -> None:
        for i in range(5):
            prod = models.Product.objects.create(name=f'test{i}', price=i+1.00, category=f'category{i}')
            models.ProductSales.objects.create(product=prod)

    def test_product_sales_creation(self):
        self.assertEqual(len(models.ProductSales.objects.all()), 5)

    def test_get_product_name(self):
        self.assertEqual(models.ProductSales.objects.get(id=1).product.name, 'test0')

    def test_get_product_price(self):
        self.assertEqual(float(models.ProductSales.objects.get(id=1).product.price), 1.00)

    def test_get_product_category(self):
        self.assertEqual(models.ProductSales.objects.get(id=1).product.category, 'category0')
