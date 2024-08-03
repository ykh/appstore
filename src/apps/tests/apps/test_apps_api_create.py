from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.models.app import App
from appstore.utils.unit_test_helpers import UnitTestHelpers
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsAPICreateTestCases(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        users_svc = UsersService()

        self.user = users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'user1@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        auth_url = reverse('auth_token')

        response = self.client.post(
            path=auth_url,
            data={
                'email': 'user1@email.com',
                'password': '123qwe!@#QWE',
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_create_app_success(self):
        url = reverse('apps-list')

        data = {
            'title': 'New App',
            'description': 'App description',
            'price': 9.99,
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_keys = (
            'id',
            'title',
            'description',
            'price',
            'icon',
            'user_id',
            'is_verified',
            'is_activated',
            'created_at',
            'updated_at',
        )

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_create_app_without_credential(self):
        url = reverse('apps-list')

        self.client.credentials()

        data = {
            'title': 'New App with Icon',
            'description': 'App description',
            'price': 9.99,
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_app_with_icon_file(self):
        url = reverse('apps-list')

        image_file = UnitTestHelpers.generate_temp_file()

        data = {
            'title': 'New App with Icon',
            'description': 'App description',
            'price': 9.99,
            'icon': image_file,
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['icon'])

        app = App.objects.get(id=response.data['id'])
        UnitTestHelpers.delete_file(app.icon.path)
