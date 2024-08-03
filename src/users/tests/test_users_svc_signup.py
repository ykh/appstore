from uuid import UUID

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService


class UsersSVCSignUpTestCases(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_signup_success(self):
        inputs = {
            'email': 'user1@email.com',
            'password': '123qwe!@#QWE',
        }

        svc = UsersService()

        user = svc.signup(
            params=UsersSVCSignUpVLD(data=inputs)
        )

        self.assertIsInstance(user, self.User)
        self.assertEqual(user.email, inputs['email'])
        self.assertIsInstance(user.id, UUID)
        self.assertTrue(user.check_password(inputs['password']))

    def test_signup_duplicated(self):
        inputs = {
            'email': 'user1@email.com',
            'password': '123qwe!@#QWE',
        }

        svc = UsersService()

        svc.signup(
            params=UsersSVCSignUpVLD(data=inputs)
        )

        with self.assertRaises(exceptions.ValidationError):
            svc.signup(
                params=UsersSVCSignUpVLD(data=inputs)
            )

    def test_signup_weak_password(self):
        inputs = {
            'email': 'user1@email.com',
            'password': '123',
        }

        svc = UsersService()

        with self.assertRaises(exceptions.ValidationError):
            svc.signup(
                params=UsersSVCSignUpVLD(data=inputs)
            )

    def test_signup_invalid_email(self):
        inputs = {
            'email': 'invalid_email',
            'password': '123qwe!@#QWE',
        }

        svc = UsersService()

        with self.assertRaises(exceptions.ValidationError):
            svc.signup(
                params=UsersSVCSignUpVLD(data=inputs)
            )

    def test_signup_blank_inputs(self):
        inputs = {
            'email': '',
            'password': '',
        }

        svc = UsersService()

        with self.assertRaises(exceptions.ValidationError):
            svc.signup(
                params=UsersSVCSignUpVLD(data=inputs)
            )
