from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCRetrieveTestCases(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        self.users_svc = UsersService()
        self.apps_svc = AppsService()

        self.user = self.users_svc.signup(
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

        app_data = {
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = self.apps_svc.create(params=app_data, requester=self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_retrieve_app_success(self):
        url = reverse('apps-detail', kwargs={'pk': self.app.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'id': str(self.app.id),
            'user_id': str(self.app.user.id),
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': '9.99',
            'icon': None,
            'is_verified': False,
            'is_activated': True,
        }

        for key, value in expected_data.items():
            self.assertEqual(value, response.data[key])
