from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError

from apps.models.purchase import Purchase
from apps.services.apps_svc import AppsService
from apps.services.purchases_svc import PurchasesService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class PurchasesSVCCreateTestCases(TestCase):
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

    def test_create_purchase_success(self):
        purchase = self.purchases_svc.create(
            params={
                'user_id': self.customer.id,
                'app_id': self.app1.id,
            },
        )

        self.assertIsInstance(purchase, Purchase)
        self.assertEqual(purchase.user, self.customer)
        self.assertEqual(purchase.app, self.app1)
        self.assertEqual(purchase.cost, self.app1.price)

        self.customer.refresh_from_db()

        self.assertEqual(self.customer.credit, Decimal(100 - self.app1.price))

    def test_create_purchase_insufficient_credit(self):
        with self.assertRaises(ValidationError) as context:
            self.purchases_svc.create(
                params={
                    'user_id': self.customer.id,
                    'app_id': self.app2.id,
                },
            )

            self.assertEqual(
                str(context.exception),
                "The user's credit is insufficient.",
            )

    def test_create_purchase_invalid_user_id(self):
        invalid_user_id = 9999

        with self.assertRaises(exceptions.ValidationError):
            self.purchases_svc.create(
                params={
                    'user': invalid_user_id,
                    'app': self.app1.id,
                },
            )

    def test_create_purchase_invalid_app_id(self):
        invalid_app_id = 9999
        with self.assertRaises(exceptions.ValidationError):
            self.purchases_svc.create(
                params={
                    'user': self.customer.id,
                    'app': invalid_app_id,
                },
            )
