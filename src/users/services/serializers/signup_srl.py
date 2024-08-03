from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from rest_framework.serializers import CharField, ModelSerializer


class UsersSVCSignUpVLD(ModelSerializer):
    """
    SignUp inputs validator.
    """
    password = CharField(
        write_only=True,
        validators=[
            MinLengthValidator(8),
            validate_password,
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password',)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user
