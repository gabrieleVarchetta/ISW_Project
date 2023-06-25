import datetime
import unittest

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

from store.models import Customer, Product, ShippingAddress, PaymentMethod


class TestUseCase001(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_001(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('login'))

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        self.fill_form_and_submit(form_data)

        welcome_message = WebDriverWait(driver, 5).until(
            ec.visibility_of_element_located((By.ID, 'welcome_message'))
        )

        self.assertTrue(welcome_message.is_displayed())

    def test_case_002(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('login'))

        form_data = {
            "username": "wakawrong",
            "password": "wakawrongpsw"
        }

        self.fill_form_and_submit(form_data)

        error_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(
                (By.XPATH,
                 "//li[contains(text(), 'Please enter a correct username and password. Note that both fields may be case-sensitive.')]"))
        )
        self.assertTrue(error_message.is_displayed())

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase002(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)

        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_003(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('register'))

        form_data = {
            "first_name": "Virgilio",
            "last_name": "Di Falco",
            "email": "virgilio@example.com",
            "password": "virgivirgi",
            "username": "flacodiwella",
            "birth_day": "02/10/2000",
            "country": "Italy",
            "region": "Sardinia",
            "city": "Domusnovas",
            "street_address": "Via Fratelli Bandiera 10",
            "postal_code": "09015",
            "province": "Sud Sardegna",
            'card_number': '1234567890123456',
            'cardholder_name': 'Virgilio Di Falco',
            'expiration_month': '5',
            'expiration_year': '23',
            'cvv': '1234'
        }

        self.fill_form_and_submit(form_data)

        success_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'msg'))
        )
        self.assertTrue(success_message.is_displayed())

    def test_case_004(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('register'))

        form_data = {
            "first_name": "Virgilio",
            "last_name": "Di Falco",
            "email": "virgilio@example.com",
            "password": "virgivirgi",
            "username": "flacodiwella",
            "birth_day": "02/10/2000",
            "country": "Italy",
            "region": "Sardinia",
            "city": "Domusnovas",
            "street_address": "Via Fratelli Bandiera 10",
            "postal_code": "09015",
            "province": "Sud Sardegna",
            'card_number': '1234567890123456',
            'cardholder_name': 'Virgilio Di Falco',
            'expiration_month': '5',
            'expiration_year': '23',
            'cvv': '1234'
        }

        self.fill_form_and_submit(form_data)

        error_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.ID, "msg"))
        )
        self.assertTrue(error_message.is_displayed())

    def tearDown(self):
        self.driver.close()


class TestUseCase003(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_005(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('login'))

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        self.fill_form_and_submit(form_data)

        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

        product_list = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "product-card"))
        )
        self.assertTrue(product_list.is_displayed())

    def test_case_006(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('products'))

        driver.get(self.live_server_url + reverse('login'))

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        self.fill_form_and_submit(form_data)

        no_product_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'No products found.')]"))
        )
        self.assertTrue(no_product_message.is_displayed())

    def test_case_007(self):
        driver = self.driver
        driver.get(self.live_server_url + reverse('products'))

        login_form = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, "//div[@id='div_id_username']"))
        )
        self.assertTrue(login_form.is_displayed())

    def tearDown(self):
        self.driver.close()


class TestUseCase004(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_008(self):
        driver = self.driver
        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        cart_items = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "cart-product-card"))
        )

        self.assertTrue(cart_items.is_displayed())

    def test_case_009(self):
        driver = self.driver

        driver.get(self.live_server_url + reverse('products'))

        try:
            add_to_cart_button = WebDriverWait(driver, 3).until(
                ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
            )
            add_to_cart_button.click()
        except TimeoutException:
            print('You are not logged in')

        self.assertTrue('login' in str(driver.current_url))

    def tearDown(self):
        self.driver.close()


class TestUseCase005(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_010(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

        time.sleep(1)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        cart_items = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "cart-product-card"))
        )

        self.assertTrue(cart_items.is_displayed())

    def test_case_011(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        empty_cart_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, "empty_cart_msg"))
        )

        self.assertTrue(empty_cart_msg.is_displayed())

    def test_case_012(self):
        driver = self.driver

        driver.get(self.live_server_url + reverse('shopping_cart'))

        try:
            cart_items = WebDriverWait(driver, 3).until(
                ec.visibility_of_element_located((By.CLASS_NAME, "cart-product-card"))
            )
        except TimeoutException:
            print('You are not logged in')

        self.assertTrue('login' in str(driver.current_url))

    def tearDown(self):
        self.driver.close()


class TestUseCase006(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_013(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        increase_quantity_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, "increase_qty"))
        )
        increase_quantity_btn.click()

        time.sleep(1)

        qty_text = driver.find_element(By.CLASS_NAME, 'quantity-section')

        self.assertTrue('2' in qty_text.text)

    def test_case_014(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        for _ in range(2):
            add_to_cart = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
            )
            add_to_cart.click()
            time.sleep(1)

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        decrease_quantity_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, "decrease_qty"))
        )
        decrease_quantity_btn.click()

        time.sleep(1)

        qty_text = driver.find_element(By.CLASS_NAME, 'quantity-section')

        self.assertTrue('1' in qty_text.text)

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase007(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        Customer.objects.create(user=User.objects.get(username='test'), birth_day=datetime.date(2001, 11, 5))
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_015(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        remove_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, "remove-button"))
        )
        remove_btn.click()

        time.sleep(1)

        no_product_msg = driver.find_element(By.ID, 'empty_cart_msg')

        self.assertTrue(no_product_msg.is_displayed())

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase008(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test')
        user = User.objects.get(username='test')
        Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))
        customer = Customer.objects.get(user=user)
        ShippingAddress.objects.create(customer=customer, country='test', region='test', city='test',
                                       street_address='test', postal_code='test', province='test',
                                       default_shipping_address=True)
        PaymentMethod.objects.create(customer=customer, card_number='1234567890123456', cardholder_name='test',
                                     expiration_month=5, expiration_year=21, cvv=1234, default_payment_method=True)
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_016(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(3)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        order_summary_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'checkout-button'))
        )
        order_summary_btn.click()

        checkout_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'complete_order'))
        )
        checkout_btn.click()

        order_completed_msg = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'msg'))
        )

        self.assertTrue(order_completed_msg.is_displayed())

    def test_case_017(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        time.sleep(1)

        add_to_cart = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'add_to_cart_button'))
        )
        add_to_cart.click()

        time.sleep(1)

        button_cart = driver.find_element(By.ID, "go_to_shopping_cart")
        button_cart.click()

        order_summary_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'checkout-button'))
        )
        order_summary_btn.click()

        payment_methods_list = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'payment_method'))
        )

        shipping_addresses_list = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'shipping_address'))
        )

        self.assertTrue(payment_methods_list.is_displayed() and shipping_addresses_list.is_displayed())

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase009(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test', last_name='test')
        user = User.objects.get(username='test')
        Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))
        for i in range(5):
            Product.objects.create(name=f'test prod{i + 1}', category=f'test cat{i + 1}',
                                   description=f'test desc{i + 1}', price=float(i) + 1.00)

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_018(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        search_form = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, 'search_product'))
        )

        search_form.send_keys('test prod3')
        time.sleep(1)

        search_btn = driver.find_element(By.CLASS_NAME, 'search-button')
        search_btn.click()

        searched_prod = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'product_name'))
        )

        self.assertTrue(searched_prod.text == 'test prod3')

    def test_case_019(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        search_form = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, 'search_product'))
        )

        search_form.send_keys('wrong prod name')
        time.sleep(1)

        search_btn = driver.find_element(By.CLASS_NAME, 'search-button')
        search_btn.click()

        no_product_message = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'No products found.')]"))
        )
        self.assertTrue(no_product_message.is_displayed())

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase010(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_user(username='test', password='testpassword1234', first_name='test', last_name='test')
        user = User.objects.get(username='test')
        Customer.objects.create(user=user, birth_day=datetime.date(2001, 11, 5))

    def fill_form_and_submit(self, form_data):
        for field_name, field_value in form_data.items():
            input_field = self.driver.find_element(By.NAME, field_name)
            input_field.send_keys(field_value)

        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

    def test_case_020(self):
        driver = self.driver

        form_data = {
            "username": "test",
            "password": "testpassword1234"
        }

        driver.get(self.live_server_url + reverse('login'))

        self.fill_form_and_submit(form_data)

        logout_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Logout')]"))
        )
        logout_btn.click()
        time.sleep(1)
        self.assertTrue('login' in driver.current_url)

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase011(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_superuser(username='admin_test', password='admin_pass_1234')

    def test_case_021(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        welcome_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, 'user-tools'))
        )

        time.sleep(2)

        self.assertTrue('admin_test' in welcome_msg.text)

    def test_case_022(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('wrong_username')
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys('wrong_password')
        password_input.send_keys(Keys.ENTER)

        error_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'errornote'))
        )

        self.assertTrue(error_msg.is_displayed())

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase012(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        User.objects.create_superuser(username='admin_test', password='admin_pass_1234')

    def test_case_023(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        products_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Products")]'))
        )
        products_link.click()

        add_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Add product")]'))
        )
        add_btn.click()

        name_input = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, 'name'))
        )
        name_input.send_keys('Nuovo prodotto')
        description_input = driver.find_element(By.NAME, 'description')
        description_input.send_keys('Descrizione del nuovo prodotto')
        category_input = driver.find_element(By.NAME, 'category')
        category_input.send_keys('Categoria nuovo prodotto')
        price_input = driver.find_element(By.NAME, 'price')
        price_input.send_keys('10.99')

        save_button = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, '_save'))
        )
        save_button.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'Nuovo prodotto'))
        )

        self.assertIsNotNone(product_link)

    def test_case_024(self):
        driver = self.driver
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        products_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Products")]'))
        )
        products_link.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
        )
        product_link.click()

        delete_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Delete")]'))
        )
        delete_btn.click()

        confirm_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, ''' //input[@value="Yes, I’m sure"] '''))
        )
        confirm_btn.click()

        try:
            deleted_prod_link = WebDriverWait(driver, 2).until(
                ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
            )
        except TimeoutException:
            deleted_prod_link = None

        self.assertIsNone(deleted_prod_link)

    def test_case_025(self):
        driver = self.driver
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        products_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Products")]'))
        )
        products_link.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
        )
        product_link.click()

        name_field = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//input[@id="id_name"]'))
        )
        name_field.send_keys('modified test prod')

        save_button = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, '_save'))
        )
        save_button.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'modified test prod'))
        )

        self.assertIsNotNone(product_link)

    def test_case_026(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Products")]'))
        )
        product_link.click()

        add_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Add product")]'))
        )
        add_btn.click()

        name_input = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, 'name'))
        )

        name_input.send_keys('test name')
        description_input = driver.find_element(By.NAME, 'description')
        description_input.send_keys('Descrizione del nuovo prodotto')

        # Invia il form
        save_button = driver.find_element(By.NAME, '_save')
        save_button.click()

        # Check if the current url is equal to the expected one, if admin made a mistake urls are equal
        self.assertEqual(driver.current_url, self.live_server_url + '/admin/store/product/add/')
        error_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'errornote'))
        )
        self.assertEqual(error_msg.text.strip(), 'Please correct the errors below.')

    def test_case_027(self):
        driver = self.driver
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        products_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Products")]'))
        )
        products_link.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
        )
        product_link.click()

        name_field = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//input[@id="id_name"]'))
        )
        name_field.clear()

        save_button = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.NAME, '_save'))
        )
        save_button.click()

        error_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'errornote'))
        )

        self.assertEqual(error_msg.text.strip(), 'Please correct the error below.')

    def test_case_028(self):
        driver = self.driver

        driver.get(self.live_server_url + '/admin/store/product/add')

        self.assertEqual(driver.current_url, self.live_server_url + '/admin/login/?next=/admin/store/product/add')

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase013(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        User.objects.create_superuser(username='admin_test', password='admin_pass_1234')
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def test_case_030(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        product_sales_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Product saless")]'))
        )
        product_sales_link.click()

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
        )

        self.assertIsNotNone(product_link)

    def test_case_031(self):
        driver = self.driver

        driver.get(self.live_server_url + '/admin/store/productsales/')

        self.assertEqual(driver.current_url, self.live_server_url + '/admin/login/?next=/admin/store/productsales/')

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase014(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        User.objects.create_superuser(username='admin_test', password='admin_pass_1234')
        Product.objects.create(name='test prod', category='test cat', description='test desc', price=10.00)

    def test_case_032(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        product_sales_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Product saless")]'))
        )
        product_sales_link.click()

        searchbar = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//input[@id="searchbar"]'))
        )
        searchbar.send_keys('test prod')

        product_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.LINK_TEXT, 'test prod'))
        )

        self.assertIsNotNone(product_link)

    def test_case_033(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        product_sales_link = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Product saless")]'))
        )
        product_sales_link.click()

        searchbar = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//input[@id="searchbar"]'))
        )
        searchbar.send_keys('non existing prod')

        search_btn = driver.find_element(By.XPATH, '//input[@value="Search"]')
        search_btn.click()

        no_prod_msg = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//p[contains(text(), "0 product saless")]'))
        )

        self.assertTrue(no_prod_msg.is_displayed())

    def test_case_034(self):
        driver = self.driver

        driver.get(self.live_server_url + '/admin/store/productsales/?q=test')

        self.assertEqual(driver.current_url,
                         self.live_server_url + '/admin/login/?next=/admin/store/productsales/%3Fq%3Dtest')


class TestUseCase015(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()
        User.objects.create_superuser(username='admin_test', password='admin_pass_1234')

    def test_case_035(self):
        driver = self.driver
        driver.get(self.live_server_url + '/admin/')
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin_test')
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys('admin_pass_1234')
        password_input.send_keys(Keys.ENTER)

        logout_btn = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Log out")]'))
        )
        logout_btn.click()

        self.assertEqual(driver.current_url, self.live_server_url + '/admin/logout/')

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
