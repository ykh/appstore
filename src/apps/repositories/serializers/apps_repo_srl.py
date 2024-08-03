from rest_framework import serializers
from rest_framework.fields import IntegerField, UUIDField

from apps.models import App


class AppsRepoCreateVLD(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


class AppsRepoUpdateVLD(serializers.ModelSerializer):
    id = UUIDField(write_only=True)

    class Meta:
        model = App
        exclude = ('user',)


class AppsRepoListVLD(serializers.Serializer):
    owner_id = serializers.UUIDField(required=False, allow_null=False)
    title = serializers.CharField(required=False, allow_null=False)
    page_number = IntegerField(required=False, default=1)
    page_size = IntegerField(required=False, default=10)
