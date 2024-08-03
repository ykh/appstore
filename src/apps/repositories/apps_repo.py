from typing import List

from django.core.cache import cache
from django.db.models import Q
from rest_framework import exceptions

from apps.models import App
from apps.repositories.serializers.apps_repo_srl import (
    AppsRepoCreateVLD,
    AppsRepoListVLD, AppsRepoUpdateVLD,
)
from appstore.utils.pagination import paginate_query
from users.models import User


class AppsRepo:
    def __init__(self, requester: User):
        self.requester = requester

    def get_app_user_id(self, app_id: str) -> str:
        cache_key = f'app_user_id_{app_id}'
        user_id = cache.get(cache_key)

        if user_id is None:
            try:
                user_id = App.objects.filter(id=app_id).values_list(
                    'user__id',
                    flat=True,
                ).get()
                cache.set(cache_key, user_id, timeout=86400)
            except App.DoesNotExist:
                raise exceptions.NotFound('App not found.')

        return user_id

    def create(self, params) -> App:
        params_vld = AppsRepoCreateVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        app = params_vld.save()

        return app

    def update(self, params, app_id: str) -> App:
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            raise exceptions.NotFound('App not found.')

        validator = AppsRepoUpdateVLD(data=params, instance=app, partial=True)
        validator.is_valid(raise_exception=True)

        app = validator.save()

        return app

    def retrieve(self, app_id: str) -> App:
        query = (
                Q(id=app_id) &
                Q(
                    (
                            Q(is_verified=True) & Q(is_activated=True)
                    ) |
                    Q(user=self.requester)
                )
        )

        try:
            return App.objects.filter(query).get()
        except App.DoesNotExist:
            raise exceptions.NotFound('App not found.')

    def list(self, params) -> List[App]:
        params_vld = AppsRepoListVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        params = params_vld.validated_data

        query = Q()

        if params.get('owner_id'):
            query &= Q(user=params.get('owner_id'))
        else:
            if not self.requester.is_superuser and not self.requester.is_staff:
                query &= Q(is_verified=True) & Q(is_activated=True)

        if params.get('id'):
            query &= Q(id=params.get('id'))

        if params.get('title'):
            query &= Q(title__icontains=params.get('title'))

        result = App.objects.filter(query)

        page = paginate_query(result, params['page_number'], params['page_size'])

        return page

    def destroy(self, app_id: str):
        try:
            app = App.objects.get(id=app_id)
            app.delete()
        except App.DoesNotExist:
            raise exceptions.NotFound('App not found.')
