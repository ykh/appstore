from typing import List

from django.db.models import Q
from rest_framework import exceptions

from apps.models.purchase import Purchase
from apps.repositories.serializers.purchases_repo_srl import (
    PurchasesRepoCreateVLD,
    PurchasesRepoListVLD,
)
from appstore.utils.pagination import paginate_query
from users.models import User


class PurchasesRepo:
    def __init__(self, requester: User):
        self.requester = requester

    def generate_app_link(self, purchase: Purchase) -> str:
        # todo: Get it from settings, or even write an API method for it.
        url = f'https://cdn.appstore.app/api/purchases/{purchase.id}/download'

        return url

    def create(self, params) -> Purchase:
        params_vld = PurchasesRepoCreateVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        v_data = params_vld.validated_data

        purchase = Purchase(**v_data)

        purchase.app_link = self.generate_app_link(purchase)

        purchase.save()

        return purchase

    def retrieve(self, purchase_id: str) -> Purchase:
        query = Q(id=purchase_id) & Q(user__id=self.requester.id)

        try:
            return Purchase.objects.filter(query).get()
        except Purchase.DoesNotExist:
            raise exceptions.NotFound('Purchase not found.')

    def list(self, params) -> List[Purchase]:
        params_vld = PurchasesRepoListVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        v_data = params_vld.validated_data

        if self.requester.is_superuser or self.requester.is_staff:
            query = Q()
        else:
            query = Q(user__id=self.requester.id)

        result = Purchase.objects.filter(query)

        page = paginate_query(result, v_data['page_number'], v_data['page_size'])

        return page
