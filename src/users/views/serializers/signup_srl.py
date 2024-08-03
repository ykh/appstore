from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from rest_framework.serializers import CharField, EmailField, Serializer, UUIDField


class UsersViewSignUpVLD(Serializer):
    """
    SignUp inputs validator.
    """
    email = EmailField()
    password = CharField(
        write_only=True,
        validators=[
            MinLengthValidator(8),
            validate_password,
        ]
    )


class UsersViewSignUpTRF(Serializer):
    """
    SignUp response transformer.
    """
    id = UUIDField()
    email = EmailField()
