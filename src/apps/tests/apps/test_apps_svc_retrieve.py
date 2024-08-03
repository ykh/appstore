from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from apps.models import App
from apps.services.apps_svc import AppsService
from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class AppsSVCRetrieveTestCases(TestCase):
    def setUp(self):
        self.apps_svc = AppsService()

        self.User = get_user_model()

        self.users_svc = UsersService()

        self.user = self.users_svc.signup(
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

    def test_retrieve_app_success(self):
        app = self.apps_svc.retrieve(
            app_id=self.app.id,
            requester=self.user,
        )

        self.assertIsInstance(app, App)
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.id, self.app.id)
        self.assertEqual(app.title, 'Test App')
        self.assertEqual(app.description, 'This is a test app.')
        self.assertEqual(str(app.price), '9.99')

    def test_retrieve_app_invalid_app_id(self):
        invalid_app_id = 'invalid_uuid'

        with self.assertRaises(exceptions.ValidationError):
            self.apps_svc.retrieve(
                app_id=invalid_app_id,
                requester=self.user,
            )

    def test_retrieve_app_not_exists(self):
        invalid_app_id = 'bb216971-abbe-46f5-b881-fbfdd394229a'

        with self.assertRaises(exceptions.NotFound):
            self.apps_svc.retrieve(
                app_id=invalid_app_id,
                requester=self.user,
            )

    def test_retrieve_app_returns_unverified_app_for_non_owner(self):
        non_owner_user = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'non-owner@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        with self.assertRaises(exceptions.NotFound):
            self.apps_svc.retrieve(
                app_id=self.app.id,
                requester=non_owner_user,
            )

    def test_retrieve_app_returns_verified_app_for_non_owner(self):
        non_owner_user = self.users_svc.signup(
            params=UsersSVCSignUpVLD(
                data={
                    'email': 'non-owner@email.com',
                    'password': '123qwe!@#QWE',
                }
            )
        )

        App.objects.filter(id=self.app.id).update(is_verified=True)

        app = self.apps_svc.retrieve(
            app_id=self.app.id,
            requester=non_owner_user,
        )

        self.assertIsInstance(app, App)
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.id, self.app.id)
