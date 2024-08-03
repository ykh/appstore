from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.services.apps_svc import AppsService
from apps.services.purchases_svc import PurchasesService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class PurchasesAPIListTestCases(APITestCase):
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

        self.vendor1 = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'vendor1@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.vendor2 = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'vendor2@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        self.app1v1 = self.apps_svc.create(
            params={
                'title': 'App1',
                'description': 'App1 summary.',
                'price': 9.99,
                'user': self.vendor1.id,
            },
            requester=self.vendor1,
        )
        self.app1v1.verify()
        self.app1v1.activate()

        self.app2v1 = self.apps_svc.create(
            params={
                'title': 'App2',
                'description': 'App2 summary.',
                'price': 9.99,
                'user': self.vendor1.id,
            },
            requester=self.vendor1,
        )
        self.app2v1.verify()
        self.app2v1.activate()

        self.app3v2 = self.apps_svc.create(
            params={
                'title': 'App3',
                'description': 'App3 summary.',
                'price': 9.99,
                'user': self.vendor2.id,
            },
            requester=self.vendor1,
        )
        self.app3v2.verify()
        self.app3v2.activate()

        self.purchases_svc.create(
            params={
                'user_id': self.customer.id,
                'app_id': self.app1v1.id,
            },
        )

        self.purchases_svc.create(
            params={
                'user_id': self.customer.id,
                'app_id': self.app3v2.id,
            },
        )

        auth_url = reverse('auth_token')

        response = self.client.post(
            path=auth_url,
            data={
                'email': 'customer@email.com',
                'password': '123qwe!@#QWE',
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_list_purchases_for_the_customer(self):
        url = reverse('purchases-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data

        self.assertEqual(len(response_data['result']), 2)

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

        for purchase in response_data['result']:
            for key in expected_keys:
                self.assertIn(key, purchase)

            self.assertEqual(purchase['user_id'], str(self.customer.id))
