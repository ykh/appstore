from rest_framework import serializers


class PurchasesViewCreateVLD(serializers.Serializer):
    app_id = serializers.UUIDField()


class PurchasesViewCreateTRF(serializers.Serializer):
    id = serializers.UUIDField()
    user_id = serializers.UUIDField(source='user.id')
    app_id = serializers.UUIDField(source='app.id')
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    app_link = serializers.URLField()
    purchased_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class PurchasesViewRetrieveTRF(PurchasesViewCreateTRF):
    pass


class PurchasesViewListTRF(PurchasesViewCreateTRF):
    pass
