from django.test import TestCase


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Marco',
            'last_name': 'Van Basten',
            'email': 'marcovan@milan.com',
            'password': 'marcolino3p',
            'username': 'bomber',
            'birth_day': '31/10/1964',
            'country': 'Netherlands',
            'region': 'Boh',
            'city': 'Utrecht',
            'street_address': 'Milanello',
            'postal_code': '208019',
            'province': 'CA'
        }

    def test_registration(self):
        pass

