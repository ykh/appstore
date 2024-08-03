from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from apps.models import App
from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCUpdateTestCases(TestCase):
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

        app_inputs = {
            'title': 'Test App',
            'description': 'This is a test app.',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = self.apps_svc.create(params=app_inputs, requester=self.user)

    def test_update_app_success(self):
        valid_data = {
            'title': 'Test App Renamed',
            'description': 'This is a updated test app.',
            'price': 10.99,
        }

        app = self.apps_svc.update(
            params=valid_data,
            app_id=self.app.id,
            requester=self.user,
        )

        app_counts = App.objects.count()

        self.assertIsInstance(app, App)
        self.assertEqual(app.title, 'Test App Renamed')
        self.assertEqual(app.description, 'This is a updated test app.')
        self.assertEqual(str(app.price), '10.99')
        self.assertEqual(App.objects.count(), app_counts)

    def test_update_app_invalid_data(self):
        invalid_price = {
            'title': 'App Name',
            'description': 'This is a test app.',
            'price': 'invalid_price',
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.update(
                params=invalid_price,
                app_id=self.app.id,
                requester=self.user,
            )

        invalid_title = {
            'title': '',
            'description': 'This is a test app.',
            'price': 9.99,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.update(
                params=invalid_title,
                app_id=self.app.id,
                requester=self.user,
            )

        invalid_desc = {
            'title': 'App Name',
            'description': '',
            'price': 9.99,
        }

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.update(
                params=invalid_desc,
                app_id=self.app.id,
                requester=self.user,
            )
