from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UsersAPISignUpTestCase(TestCase):
    def setUp(self):
        self.url = reverse('users-signup')

    def test_signup_success(self):
        inputs = {
            'email': 'user100@email.com',
            'password': '123qwe!@#QWE'
        }

        response = self.client.post(self.url, inputs)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], inputs['email'])

    def test_signup_invalid_email(self):
        inputs = {
            'email': 'invalid_email',
            'password': '123qwe!@#QWE'
        }

        response = self.client.post(self.url, inputs)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_blank_data(self):
        inputs = {
            'email': '',
            'password': '',
        }

        response = self.client.post(self.url, inputs)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
