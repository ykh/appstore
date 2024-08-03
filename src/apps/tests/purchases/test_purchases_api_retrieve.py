from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.services.apps_svc import AppsService
from apps.services.purchases_svc import PurchasesService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class PurchasesAPIRetrieveTestCases(APITestCase):
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

        self.purchase1 = self.purchases_svc.create(
            params={
                'user_id': self.customer.id,
                'app_id': self.app2v1.id,
            },
        )

        self.purchase2 = self.purchases_svc.create(
            params={
                'user_id': self.customer.id,
                'app_id': self.app3v2.id,
            },
        )

        self.purchase3 = self.purchases_svc.create(
            params={
                'user_id': self.vendor1.id,
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

    def test_retrieve_purchase_by_its_buyer(self):
        url = reverse('purchases-detail', kwargs={'pk': self.purchase1.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        self.assertEqual(response.data['id'], str(self.purchase1.id))
        self.assertEqual(response.data['user_id'], str(self.customer.id))
        self.assertEqual(response.data['app_id'], str(self.app2v1.id))

    def test_retrieve_purchase_it_is_not_its_buyer(self):
        url = reverse('purchases-detail', kwargs={'pk': self.purchase3.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
