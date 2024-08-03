from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from apps.models import App
from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCCreateTestCases(TestCase):
    def setUp(self):
        self.apps_svc = AppsService()

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

    def test_create_app_success(self):
        valid_input = {
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        app_counts = App.objects.count()

        app = self.apps_svc.create(params=valid_input, requester=self.user)

        self.assertIsInstance(app, App)
        self.assertEqual(app.title, 'Test App')
        self.assertEqual(app.description, 'This is a test app.')
        self.assertEqual(str(app.price), '9.99')
        self.assertEqual(App.objects.count(), app_counts + 1)

    def test_create_app_invalid_data(self):
        invalid_price = {
            'title': 'App Name',
            'description': 'This is a test app.',
            'price': 'invalid_price',
            'user': self.user.id,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.create(params=invalid_price, requester=self.user)

        invalid_title = {
            'title': '',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.create(params=invalid_title, requester=self.user)

        invalid_desc = {
            'title': 'App Name',
            'description': '',
            'price': 9.99,
            'user': self.user.id,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.create(params=invalid_desc, requester=self.user)

        invalid_user = {
            'title': 'App Name',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': 1000,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.create(params=invalid_user, requester=self.user)

    def test_create_app_should_not_be_verified_by_default(self):
        valid_inputs = {
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        app = self.apps_svc.create(params=valid_inputs, requester=self.user)

        self.assertFalse(app.is_verified)
