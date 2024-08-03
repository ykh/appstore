from rest_framework import serializers


class AppsViewCreateTRF(serializers.Serializer):
    """
    Transformer for creating app API response.
    """
    id = serializers.UUIDField()
    user_id = serializers.UUIDField(source='user.id')
    title = serializers.CharField(max_length=255, )
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    icon = serializers.ImageField(required=False, allow_null=True)
    is_verified = serializers.BooleanField()
    is_activated = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AppsViewUpdateTRF(AppsViewCreateTRF):
    """
    Transformer for updating app API response.
    """
    pass


class AppsViewRetrieveTRF(AppsViewCreateTRF):
    """
    Transformer for updating app API response.
    """
    pass


class AppsViewListTRF(AppsViewCreateTRF):
    """
    Transformer for updating app API response.
    """
    pass
