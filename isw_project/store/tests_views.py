# from django.contrib.messages import get_messages
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.test import RequestFactory, TestCase
# from django.contrib.auth.models import User
# from django.urls import reverse
# from .models import Product, Customer, ShoppingCart, CartProduct, Order, OrderProduct
# from .views import CustomerLoginView, CartView, FilterProductsView
#
#
# class CustomerLoginViewTest(TestCase):
#     def setUp(self):
#         self.username = 'wakaflocka17'
#         self.password = 'wakawakapassword'
#         self.user = User.objects.create_user(username=self.username, password=self.password)
#
#         self.factory = RequestFactory()
#         self.request = self.factory.post(reverse('login'), data={'username': self.username, 'password': self.password})
#
#         middleware = SessionMiddleware()
#         middleware.process_request(self.request)
#         self.request.session.save()
#
#     def test_customer_login_view_success(self):
#         response = CustomerLoginView.as_view()(self.request)
#
#         self.assertRedirects(response, reverse('products'))
#
#         self.assertTrue(self.request.user.is_authenticated)
#
#         storage = get_messages(self.request)
#         messages_list = [m.message for m in storage]
#         self.assertIn('You have been logged in successfully.', messages_list)
#
#     def test_customer_login_view_invalid_credentials(self):
#         self.request.POST['password'] = 'wrongwakawakapassword'
#
#         response = CustomerLoginView.as_view()(self.request)
#
#         self.assertEqual(response.status_code, 200)
#
#         self.assertFalse(self.request.user.is_authenticated)
#
#         storage = get_messages(self.request)
#         messages_list = [m.message for m in storage]
#         self.assertIn('Invalid username or password.', messages_list)
#
#
# # class RegistrationViewTest(TestCase):
# #     def setUp(self):
# #         self.data = {
# #             'first_name': 'Marco',
# #             'last_name': 'Van Basten',
# #             'email': 'marcovan@milan.com',
# #             'password': 'marcolino3p',
# #             'username': 'bomber',
# #             'birth_day': '31/10/1964',
# #             'country': 'Netherlands',
# #             'region': 'Boh',
# #             'city': 'Utrecht',
# #             'street_address': 'Milanello',
# #             'postal_code': '208019',
# #             'province': 'CA'
# #         }
# #
# #     def test_registration(self):
# #         pass
# #
# #
# # class CartViewTest(TestCase):
# #     def setUp(self):
# #         self.username = 'wakaflocka17'
# #         self.password = 'wakawakapassword'
# #         self.user = User.objects.create_user(username=self.username, password=self.password)
# #         self.customer = Customer.objects.create(user=self.user)
# #
# #         self.product = Product.objects.create(name='iPhone 14 PRO', price=17.17)
# #
# #         self.factory = RequestFactory()
# #         self.request = self.factory.get(reverse('shopping_cart'))
# #         self.request.user = self.user
# #
# #         middleware = SessionMiddleware()
# #         middleware.process_request(self.request)
# #         self.request.session.save()
# #
# #     def test_cart_view_product_list(self):
# #         response = CartView.product_list(self.request)
# #
# #         self.assertEqual(response.status_code, 200)
# #
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.get(shoppingcart=shopping_cart, product=self.product)
# #         self.assertIn(cart_product, shopping_cart.products.all())
# #
# #     def test_cart_view_add_to_cart(self):
# #         self.request.method = 'POST'
# #         self.request.POST['product_id'] = str(self.product.id)
# #
# #         response = CartView.add_to_cart(self.request, self.product.id)
# #
# #         self.assertRedirects(response, reverse('products'))
# #
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.get(shoppingcart=shopping_cart, product=self.product)
# #         self.assertIn(cart_product, shopping_cart.products.all())
# #
# #         storage = get_messages(self.request)
# #         messages_list = [m.message for m in storage]
# #         self.assertIn('Product added to cart!', messages_list)
# #
# #     def test_cart_view_delete_from_cart(self):
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.create(shoppingcart=shopping_cart, product=self.product)
# #
# #         self.request.method = 'POST'
# #         self.request.POST['product_id'] = str(cart_product.id)
# #
# #         response = CartView.delete_from_cart(self.request, cart_product.id)
# #
# #         self.assertRedirects(response, reverse('shopping_cart'))
# #
# #         self.assertNotIn(cart_product, shopping_cart.products.all())
# #
# #         storage = get_messages(self.request)
# #         messages_list = [m.message for m in storage]
# #         self.assertIn('Product has been deleted!', messages_list)
# #
# #     def test_cart_view_increase_product_quantity(self):
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.create(shoppingcart=shopping_cart, product=self.product)
# #
# #         self.request.method = 'POST'
# #         self.request.POST['product_id'] = str(cart_product.id)
# #
# #         response = CartView.increase_product_quantity(self.request, cart_product.id)
# #
# #         self.assertRedirects(response, reverse('shopping_cart'))
# #
# #         cart_product.refresh_from_db()
# #         self.assertEqual(cart_product.quantity, 2)
# #
# #     def test_cart_view_decrease_product_quantity(self):
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.create(shoppingcart=shopping_cart, product=self.product, quantity=2)
# #
# #         self.request.method = 'POST'
# #         self.request.POST['product_id'] = str(cart_product.id)
# #
# #         response = CartView.decrease_product_quantity(self.request, cart_product.id)
# #
# #         self.assertRedirects(response, reverse('shopping_cart'))
# #
# #         cart_product.refresh_from_db()
# #         self.assertEqual(cart_product.quantity, 1)
# #
# #     def test_cart_view_decrease_product_quantity_remove_product(self):
# #         shopping_cart = ShoppingCart.objects.get(customer=self.customer)
# #         cart_product = CartProduct.objects.create(shoppingcart=shopping_cart, product=self.product, quantity=1)
# #
# #         self.request.method = 'POST'
# #         self.request.POST['product_id'] = str(cart_product.id)
# #
# #         response = CartView.decrease_product_quantity(self.request, cart_product.id)
# #
# #         self.assertRedirects(response, reverse('shopping_cart'))
# #
# #         self.assertNotIn(cart_product, shopping_cart.products.all())
# #
# #
# # class FilterProductsViewTest(TestCase):
# #     def setUp(self):
# #         self.product1 = Product.objects.create(name='iPhone 14 PRO', category='Electronics', price=17.17)
# #         self.product2 = Product.objects.create(name='iPhone XS', category='Electronics', price=20.0)
# #         self.product3 = Product.objects.create(name='Pasta', category='Food', price=15.0)
# #
# #         self.factory = RequestFactory()
# #
# #     def get_filtered_response(self, params=None):
# #         self.request = self.factory.get(reverse('filter_products'), params)
# #         return FilterProductsView.as_view()(self.request)
# #
# #     def test_filter_products_view_without_filters(self):
# #         response = self.get_filtered_response()
# #
# #         self.assertEqual(response.status_code, 200)
# #
# #         context = response.context_data
# #         product_list = context['product_list']
# #         self.assertIn(self.product1, product_list)
# #         self.assertIn(self.product2, product_list)
# #         self.assertIn(self.product3, product_list)
# #
# #         categories = context['categories']
# #         self.assertIn('Electronics', categories)
# #         self.assertIn('Food', categories)
# #
# #     def test_filter_products_view_with_search_filter(self):
# #         response = self.get_filtered_response({'search_product': 'iPhone'})
# #
# #         self.assertEqual(response.status_code, 200)
# #
# #         context = response.context_data
# #         product_list = context['product_list']
# #         self.assertIn(self.product1, product_list)
# #         self.assertIn(self.product2, product_list)
# #         self.assertNotIn(self.product3, product_list)
# #
# #     def test_filter_products_view_with_category_filter(self):
# #         response = self.get_filtered_response({'filter_category': 'Electronics'})
# #
# #         self.assertEqual(response.status_code, 200)
# #
# #         context = response.context_data
# #         product_list = context['product_list']
# #         self.assertIn(self.product1, product_list)
# #         self.assertIn(self.product2, product_list)
# #         self.assertNotIn(self.product3, product_list)
# #
# #     def test_filter_products_view_with_ordering(self):
# #         response = self.get_filtered_response({'order_by': 'price'})
# #
# #         self.assertEqual(response.status_code, 200)
# #
# #         context = response.context_data
# #         product_list = context['product_list']
# #         self.assertEqual(list(product_list), [self.product1, self.product3, self.product2])
# #
# #
# # class CheckoutViewTestCase(TestCase):
# #     def setUp(self):
# #         self.user = User.objects.create_user(username='wakaflocka17', password='wakawakapassword')
# #         self.customer = Customer.objects.create(user=self.user)
# #         self.shopping_cart = ShoppingCart.objects.create(customer=self.customer)
# #         self.product = Product.objects.create(name='Apple Pencil', price=17.17)
# #         self.shopping_cart.add_to_cart(self.product)
# #
# #     def test_summary(self):
# #         self.client.force_login(self.user)
# #         response = self.client.get(reverse('summary'))
# #         self.assertEqual(response.status_code, 200)
# #
# #         order = Order.objects.get(customer=self.customer)
# #         order_product = OrderProduct.objects.get(order=order)
# #
# #         self.assertEqual(order_product.product, self.product)
# #         self.assertEqual(order_product.quantity, 1)
# #         self.assertEqual(order.price, self.shopping_cart.get_cart_total())
# #
# #     def test_checkout(self):
# #         self.client.force_login(self.user)
# #         response = self.client.post(reverse('checkout'))
# #         self.assertEqual(response.status_code, 302)
# #         self.assertRedirects(response, reverse('products'))
# #
# #         order = Order.objects.get(customer=self.customer)
# #         self.assertFalse(ShoppingCart.objects.filter(customer=self.customer).exists())
# #         self.assertEqual(order.pending, True)
# #
# #         messages = list(response.wsgi_request._messages)
# #         self.assertEqual(len(messages), 1)
# #         self.assertEqual(str(messages[0]), 'Order completed successfully')
