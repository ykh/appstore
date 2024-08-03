from typing import List

from rest_framework import exceptions

from apps.models import App
from apps.permissions import app_permissions
from apps.repositories.apps_repo import AppsRepo
from apps.services.serializers.apps_srl import (
    AppsSVCCreateVLD,
    AppsSVCListVLD,
    AppsSVCUpdateVLD,
)
from appstore.utils.singleton import singleton
from appstore.utils.validators import validate_uuid
from users.models import User


@singleton
class AppsService:
    def create(self, params, requester: User) -> App:
        app_permissions.has_create_permission(user=requester)

        params_vld = AppsSVCCreateVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        apps_repo = AppsRepo(requester=requester)

        return apps_repo.create(params=params_vld.validated_data)

    @validate_uuid(
        'app_id',
        exception=exceptions.ValidationError,
        message='Given app_id is not valid.',
    )
    def update(self, params, app_id: str, requester: User) -> App:
        params_vld = AppsSVCUpdateVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        apps_repo = AppsRepo(requester=requester)

        app_user_id = apps_repo.get_app_user_id(app_id=app_id)

        app_permissions.has_update_permission(app_user_id=app_user_id, user=requester)

        app_user_id = apps_repo.update(
            params=params_vld.validated_data,
            app_id=app_id,
        )

        return app_user_id

    @validate_uuid(
        'app_id',
        exception=exceptions.ValidationError,
        message='Given app_id is not valid.',
    )
    def destroy(self, app_id: str, requester: User) -> None:
        apps_repo = AppsRepo(requester=requester)

        app_user_id = apps_repo.get_app_user_id(app_id=app_id)

        app_permissions.has_destroy_permission(app_user_id=app_user_id, user=requester)

        return apps_repo.destroy(app_id=app_id)

    @validate_uuid(
        'app_id',
        exception=exceptions.ValidationError,
        message='Given app_id is not valid.',
        is_optional=True,
    )
    def retrieve(self, app_id: str, requester: User) -> App:
        app_permissions.has_retrieve_permission(user=requester)

        apps_repo = AppsRepo(requester=requester)

        return apps_repo.retrieve(app_id=app_id)

    def list(self, params, requester: User) -> List[App]:
        app_permissions.has_list_permission(user=requester)

        params_vld = AppsSVCListVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        apps_repo = AppsRepo(requester=requester)

        return apps_repo.list(params=params_vld.validated_data)
