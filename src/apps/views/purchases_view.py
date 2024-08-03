from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.services.purchases_svc import PurchasesService
from apps.views.serializers.purchases_srl import (
    PurchasesViewCreateTRF,
    PurchasesViewCreateVLD, PurchasesViewListTRF, PurchasesViewRetrieveTRF,
)
from appstore.utils.pagination import paginate_response


class PurchasesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.purchases_svc = PurchasesService()

    def list(self, request):
        paginated_result = self.purchases_svc.list(
            params=request.query_params,
            requester=request.user,
        )

        return Response(
            paginate_response(
                data=PurchasesViewListTRF(
                    instance=paginated_result.object_list,
                    many=True,
                ).data,
                paginated_result=paginated_result,
            )
        )

    def create(self, request):
        request_vld = PurchasesViewCreateVLD(data=request.data)
        request_vld.is_valid(raise_exception=True)

        purchase = self.purchases_svc.create(
            params={
                **request_vld.validated_data,
                'user_id': request.user.id,
            },
        )

        return Response(
            PurchasesViewCreateTRF(instance=purchase).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        result = self.purchases_svc.retrieve(
            purchase_id=pk,
            requester=request.user,
        )

        return Response(
            PurchasesViewRetrieveTRF(instance=result).data,
            status=status.HTTP_200_OK,
        )
