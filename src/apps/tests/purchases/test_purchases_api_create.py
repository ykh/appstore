from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.services.apps_svc import AppsService
from apps.services.purchases_svc import PurchasesService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class PurchasesAPICreateTestCases(APITestCase):
    def setUp(self):
        self.apps_svc = AppsService()
        self.purchases_svc = PurchasesService()
        self.users_svc = UsersService()

        self.User = get_user_model()

        self.customer = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'customer@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.vendor = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'vendor@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.app1 = self.apps_svc.create(
            params={
                'title': 'App1',
                'description': 'App1 summary.',
                'price': 9.99,
                'user': self.vendor.id,
            },
            requester=self.vendor,
        )
        self.app1.verify()
        self.app1.activate()

        self.app2 = self.apps_svc.create(
            params={
                'title': 'App2',
                'description': 'App2 summary.',
                'price': 199.99,
                'user': self.vendor.id,
            },
            requester=self.vendor,
        )
        self.app2.verify()
        self.app2.activate()

        auth_url = reverse('auth_token')

        response = self.client.post(
            path=auth_url,
            data={
                'email': 'customer@email.com',
                'password': '123qwe!@#QWE',
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_create_purchase_success(self):
        url = reverse('purchases-list')

        data = {
            'app_id': self.app1.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_keys = (
            'id',
            'user_id',
            'app_id',
            'cost',
            'app_link',
            'purchased_at',
            'created_at',
            'updated_at',
        )

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_create_purchase_twice_for_one_app(self):
        url = reverse('purchases-list')

        data = {
            'app_id': self.app1.id,
        }

        # First purchase.
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to purchase the same app again.
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_for_deactivated_app(self):
        self.app2.is_activated = False
        self.app2.save()

        url = reverse('purchases-list')

        data = {
            'app_id': self.app2.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_purchase_for_unverified_app(self):
        self.app2.is_verified = False
        self.app2.save()

        url = reverse('purchases-list')

        data = {
            'app_id': self.app2.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_purchase_by_the_owner_of_app(self):
        auth_url = reverse('auth_token')

        response = self.client.post(
            path=auth_url,
            data={
                'email': 'vendor@email.com',
                'password': '123qwe!@#QWE',
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

        url = reverse('purchases-list')

        data = {
            'app_id': self.app1.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
