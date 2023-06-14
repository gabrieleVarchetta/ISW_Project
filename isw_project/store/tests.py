from django.test import LiveServerTestCase
import unittest
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TestUseCase012(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Safari()

    def test_case_027(self):
        # Accedi come amministratore
        self.driver.get(self.live_server_url + '/admin/')
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('admin')
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys('password')
        password_input.send_keys(Keys.ENTER)

        # Vai alla pagina di gestione dei prodotti
        self.driver.get(self.live_server_url + '/admin/products/')
        add_product_link = self.driver.find_element(By.LINK_TEXT, 'Aggiungi prodotto')
        add_product_link.click()

        # Compila il form per aggiungere un nuovo prodotto
        name_input = self.driver.find_element(By.NAME, 'name')
        name_input.send_keys('Nuovo prodotto')
        description_input = self.driver.find_element(By.NAME, 'description')
        description_input.send_keys('Descrizione del nuovo prodotto')
        price_input = self.driver.find_element(By.NAME, 'price')
        price_input.send_keys('10.99')

        # Invia il form
        save_button = self.driver.find_element(By.NAME, '_save')
        save_button.click()

        # Verifica che il prodotto sia stato aggiunto correttamente
        product_link = self.driver.find_element(By.LINK_TEXT, 'Nuovo prodotto')
        self.assertIsNotNone(product_link)
    def tearDown(self) -> None:
        self.driver.close()


# Create your tests here.
