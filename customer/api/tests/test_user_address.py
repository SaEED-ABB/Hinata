from django.test import TestCase

import json

from customer.models import User


class UserAddAddressTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone_number="09153627719", password="1234qwer", first_name="a", last_name="b")

        cls.ADD_ADDRESS_PATH = '/api/customer/add_address/'
        cls.ADD_ADDRESS_DATA = {
            'address': 'Qaen faaze4',
            'phone_number': '4321'
        }

        cls.GET_ADDRESS_PATH = '/api/customer/get_addresses/'

        cls.DELETE_ADDRESS_PATH = '/api/customer/delete_address/'
        cls.DELETE_ADDRESS_DATA = {
            'address_id': 1
        }

    def setUp(self):
        self.client.login(phone_number=self.user.phone_number, password="1234qwer")

    def test_add_address(self):
        response = self.client.post(path=self.ADD_ADDRESS_PATH,
                                    data=self.ADD_ADDRESS_DATA,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 201)

    def test_get_addresses(self):
        self.client.post(path=self.ADD_ADDRESS_PATH,
                         data=self.ADD_ADDRESS_DATA,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get(path=self.GET_ADDRESS_PATH,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

    def test_delete_address(self):
        self.client.post(path=self.ADD_ADDRESS_PATH,
                         data=self.ADD_ADDRESS_DATA,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(path=self.DELETE_ADDRESS_PATH,
                                    data=self.DELETE_ADDRESS_DATA,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 204)
