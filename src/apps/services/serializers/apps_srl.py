from decimal import Decimal

from rest_framework import serializers

from apps.models import App


class AppsSVCCreateVLD(serializers.Serializer):
    user = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal(0),
    )
    icon = serializers.ImageField(required=False)


class AppsSVCUpdateVLD(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=False,
        allow_null=False,
    )
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal(0),
        required=False,
        allow_null=False,
    )
    icon = serializers.ImageField(required=False, allow_null=True)


class AppsSVCListVLD(serializers.Serializer):
    owner_id = serializers.UUIDField(required=False)
    title = serializers.CharField(required=False)
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)


class AppsSVCCreateTRF(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'
