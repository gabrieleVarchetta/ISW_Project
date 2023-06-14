import unittest
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TestUseCase006(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_014(self):
        driver = self.driver
        driver.get(self.live_server_url+reverse('shopping_cart'))
        elem = driver.find_element(By.CLASS_NAME, 'da_inserire')
        elem.send_keys('5')
        elem.send_keys(Keys.ENTER)
        self.assertEqual(elem.text, '5')
        time.sleep(2)

    def test_case_015(self):
        driver = self.driver
        driver.get(self.live_server_url+reverse('shopping_cart'))
        elem = driver.find_element(By.CLASS_NAME, 'da_inserire')
        elem.send_keys('-1')
        elem.send_keys(Keys.ENTER)
        banner = driver.find_element(By.ID, 'da_inserire')
        self.assertEqual('Invalid quantity.', banner.text)
        time.sleep(2)

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase007(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_016(self):
        driver = self.driver
        driver.get(self.live_server_url+reverse('shopping_cart'))
        button = driver.find_element(By.CLASS_NAME, 'da_inserire')
        products = driver.find_elements(By.CLASS_NAME, 'product')
        old_len = len(products)
        button.send_keys(Keys.ENTER)
        confirm_btn = driver.find_element(By.ID, 'da_inserire')
        confirm_btn.send_keys(Keys.ENTER)
        products = driver.find_elements(By.CLASS_NAME, 'product')
        self.assertEqual(len(products), old_len - 1)
        time.sleep(2)

    def test_case_017(self):
        driver = self.driver
        driver.get(self.live_server_url+reverse('shopping_cart'))
        button = driver.find_element(By.CLASS_NAME, 'da_inserire')
        products = driver.find_elements(By.CLASS_NAME, 'product')
        old_len = len(products)
        button.send_keys(Keys.ENTER)
        cancel_btn = driver.find_element(By.ID, 'da_inserire')
        cancel_btn.send_keys(Keys.ENTER)
        products = driver.find_elements(By.CLASS_NAME, 'product')
        self.assertEqual(len(products), old_len)
        time.sleep(2)

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase008(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_018(self):
        pass

    def test_case_019(self):
        pass

    def test_case_020(self):
        pass

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase009(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_021(self):
        pass

    def test_case_022(self):
        pass

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase010(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_023(self):
        pass

    def test_case_024(self):
        pass

    def tearDown(self) -> None:
        self.driver.close()


class TestUseCase011(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Safari()

    def test_case_025(self):
        pass

    def test_case_026(self):
        pass

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()

# class TestUseCase012(LiveServerTestCase):
#     def setUp(self):
#         self.driver = webdriver.Safari()

#     def test_case_027(self):
#         # Accedi come amministratore
#         self.driver.get(self.live_server_url + '/admin/')
#         username_input = self.driver.find_element(By.NAME, 'username')
#         username_input.send_keys('admin')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         password_input.send_keys('password')
#         password_input.send_keys(Keys.ENTER)

#         # Vai alla pagina di gestione dei prodotti
#         self.driver.get(self.live_server_url + '/admin/products/')
#         add_product_link = self.driver.find_element(By.LINK_TEXT, 'Aggiungi prodotto')
#         add_product_link.click()

#         # Compila il form per aggiungere un nuovo prodotto
#         name_input = self.driver.find_element(By.NAME, 'name')
#         name_input.send_keys('Nuovo prodotto')
#         description_input = self.driver.find_element(By.NAME, 'description')
#         description_input.send_keys('Descrizione del nuovo prodotto')
#         price_input = self.driver.find_element(By.NAME, 'price')
#         price_input.send_keys('10.99')

#         # Invia il form
#         save_button = self.driver.find_element(By.NAME, '_save')
#         save_button.click()

#         # Verifica che il prodotto sia stato aggiunto correttamente
#         product_link = self.driver.find_element(By.LINK_TEXT, 'Nuovo prodotto')
#         self.assertIsNotNone(product_link)
#     def tearDown(self) -> None:
#         self.driver.close()


