from rest_framework import serializers
from rest_framework.fields import IntegerField, UUIDField

from apps.models.purchase import Purchase


class PurchasesRepoCreateVLD(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('user', 'app', 'cost',)


class PurchasesRepoUpdateVLD(serializers.ModelSerializer):
    id = UUIDField(write_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'


class PurchasesRepoListVLD(serializers.Serializer):
    page_number = IntegerField(required=False, default=1)
    page_size = IntegerField(required=False, default=10)
