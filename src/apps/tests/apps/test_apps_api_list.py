from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.models import App
from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCRetrieveTestCases(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        self.users_svc = UsersService()
        self.apps_svc = AppsService()

        self.user1 = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'user1@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.user2 = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'user2@email.com',
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

        self.app1 = self.apps_svc.create(
            params={
                'title': 'Test App 1',
                'description': 'This is a test app.',
                'price': 9.99,
                'user': self.user1.id,
            },
            requester=self.user1,
        )

        self.app2 = self.apps_svc.create(
            params={
                'title': 'Test App 2',
                'description': 'This is a test app.',
                'price': 9.99,
                'user': self.user1.id,
            },
            requester=self.user1,
        )

        self.app3 = self.apps_svc.create(
            params={
                'title': 'Test App 3',
                'description': 'This is a test app.',
                'price': 9.99,
                'user': self.user2.id,
            },
            requester=self.user2,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_list_apps_success_without_paginate_params(self):
        App.objects.all().update(
            is_verified=True,
            is_activated=True,
        )

        url = reverse('apps-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['result']), 3)
