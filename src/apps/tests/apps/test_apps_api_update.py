from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsAPIUpdateTestCases(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        self.users_svc = UsersService()
        apps_svc = AppsService()

        self.user = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'user1@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.bad_user = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'bad_user@email.com',
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

        app_data = {
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = apps_svc.create(params=app_data, requester=self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_update_app_is_not_owner(self):
        auth_url = reverse('auth_token')

        response = self.client.post(
            path=auth_url,
            data={
                'email': 'bad_user@email.com',
                'password': '123qwe!@#QWE',
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

        url = reverse('apps-detail', kwargs={'pk': self.app.id})

        data = {
            'title': 'New App Renamed',
        }

        response = self.client.patch(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_app_is_owner(self):
        url = reverse('apps-detail', kwargs={'pk': self.app.id})

        data = {
            'title': 'New App Renamed',
        }

        response = self.client.patch(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_app_success(self):
        url = reverse('apps-detail', kwargs={'pk': self.app.id})

        data = {
            'title': 'New App Renamed',
            'description': 'App description updated.',
            'price': 10.99,
        }

        response = self.client.patch(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        expected_values = {
            'id': str(self.app.id),
            'title': data['title'],
            'description': data['description'],
            'price': str(data['price']),
        }

        for key, value in expected_values.items():
            self.assertEqual(response.data[key], value)
