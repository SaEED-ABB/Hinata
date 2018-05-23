from django.test import TestCase

from customer.models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone_number="09153627719",
                                            password="1234qwer", first_name="saeed", last_name="abbasi")

        cls.SIGNUP_PATH = '/api/customer/register/'
        cls.SIGNUP_DATA = {
            'phone_number': '123',
            'first_name': 'a',
            'last_name': 'b',
            'password1': '1234qwer',
            'password2': '1234qwer'
        }

        cls.LOGIN_PATH = '/api/customer/login/'
        cls.LOGIN_DATA = {
            'phone_number': '09153627719',
            'password': '1234qwer'
        }

        cls.LOGOUT_PATH = '/api/customer/logout/'

        cls.EDIT_USER_PATH = '/api/customer/edit_user/'
        cls.EDIT_USER_DATA = {
            'phone_number': '321',
            'first_name': 'javad',
            'last_name': 'ahmadi',
        }

        cls.GET_USER_INFO_PATH = '/api/customer/get_user_info/'

    def setUp(self):
        self.client.login(phone_number=self.user.phone_number, password="1234qwer")

    def test_signup(self):
        response = self.client.post(path=self.SIGNUP_PATH,
                                    data=self.SIGNUP_DATA,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post(path=self.LOGIN_PATH,
                                    data=self.LOGIN_DATA,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)

    def test_logout(self):
        response = self.client.get(path=self.LOGOUT_PATH)
        self.assertRedirects(response, '/')

    def test_edit_user(self):
        response = self.client.post(path=self.EDIT_USER_PATH,
                                    data=self.EDIT_USER_DATA,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)

    def test_get_user_info(self):
        response = self.client.get(path=self.GET_USER_INFO_PATH)
        self.assertEqual(response.status_code, 200)



