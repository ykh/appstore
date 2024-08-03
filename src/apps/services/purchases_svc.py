from typing import List

from django.db import transaction
from rest_framework import exceptions

from apps.models.purchase import Purchase
from apps.permissions import purchase_permissions
from apps.repositories.apps_repo import AppsRepo
from apps.repositories.purchases_repo import PurchasesRepo
from apps.services.serializers.purchases_srl import (
    PurchasesSVCCreateVLD,
    PurchasesSVCListVLD,
)
from appstore.utils.singleton import singleton
from appstore.utils.validators import validate_uuid
from users.models import User


@singleton
class PurchasesService:
    def create(self, params) -> Purchase:
        params_vld = PurchasesSVCCreateVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        v_data = params_vld.validated_data

        customer = User.objects.get(id=v_data['user_id'])

        apps_repo = AppsRepo(requester=customer)
        app = apps_repo.retrieve(app_id=v_data['app_id'])

        purchase_permissions.has_create_permission(customer=customer, app=app)

        if Purchase.objects.is_app_already_purchased_by_user(
                app_id=app.id,
                user_id=customer.id,
        ):
            raise exceptions.ValidationError('You have already purchased this app.')

        if customer.credit < app.price:
            raise exceptions.ValidationError("The customer's credit is insufficient.")

        purchases_repo = PurchasesRepo(requester=customer)

        with transaction.atomic():
            purchase = purchases_repo.create(
                params={
                    'user': customer.id,
                    'app': app.id,
                    'cost': app.price,
                }
            )

            customer.credit -= app.price
            customer.save()

        return purchase

    @validate_uuid(
        'purchase_id',
        exception=exceptions.ValidationError,
        message='Given purchase_id is not valid.',
        is_optional=True,
    )
    def retrieve(self, purchase_id: str, requester: User) -> Purchase:
        purchases_repo = PurchasesRepo(requester=requester)

        purchase = purchases_repo.retrieve(purchase_id=purchase_id)

        return purchase

    def list(self, params, requester: User) -> List[Purchase]:
        params_vld = PurchasesSVCListVLD(data=params)
        params_vld.is_valid(raise_exception=True)

        purchase_repo = PurchasesRepo(requester=requester)

        return purchase_repo.list(params=params_vld.validated_data)
