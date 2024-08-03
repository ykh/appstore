from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from apps.models import App
from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCDeleteTestCases(TestCase):
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

        self.apps_svc = AppsService()

    def test_delete_app_success(self):
        app_inputs = {
            'title': 'App1',
            'description': 'Description!',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = self.apps_svc.create(params=app_inputs, requester=self.user)

        app_counts = App.objects.count()

        self.apps_svc.destroy(
            app_id=self.app.id,
            requester=self.user,
        )

        self.assertEqual(App.objects.count(), app_counts - 1)

    def test_delete_app_invalid_app_id(self):
        app_inputs = {
            'title': 'App2',
            'description': 'Description!',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = self.apps_svc.create(params=app_inputs, requester=self.user)

        with self.assertRaises(exceptions.NotFound):
            invalid_app_id = '612ed342-5c3e-46a9-89c5-5a47160e0f69'
            self.apps_svc.destroy(
                app_id=invalid_app_id,
                requester=self.user,
            )

        app_inputs = {
            'title': 'App3',
            'description': 'Description!',
            'price': 9.99,
            'user': self.user.id,
        }

        self.app = self.apps_svc.create(params=app_inputs, requester=self.user)

        with self.assertRaises(exceptions.ValidationError):
            invalid_app_id = '1000'
            self.apps_svc.destroy(
                app_id=invalid_app_id,
                requester=self.user,
            )
