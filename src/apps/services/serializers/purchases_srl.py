from rest_framework import serializers


class PurchasesSVCCreateVLD(serializers.Serializer):
    app_id = serializers.UUIDField()
    user_id = serializers.UUIDField()


class PurchasesSVCListVLD(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
