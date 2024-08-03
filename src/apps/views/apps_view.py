from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.services.apps_svc import AppsService
from apps.views.serializers.apps_srl import (
    AppsViewCreateTRF,
    AppsViewListTRF,
    AppsViewRetrieveTRF,
)
from appstore.utils.pagination import paginate_response


class AppsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.apps_svc = AppsService()

    def list(self, request):
        paginated_result = self.apps_svc.list(
            params=request.query_params,
            requester=request.user,
        )

        return Response(
            paginate_response(
                data=AppsViewListTRF(
                    instance=paginated_result.object_list,
                    many=True,
                ).data,
                paginated_result=paginated_result,
            )
        )

    def create(self, request):
        app = self.apps_svc.create(
            params={
                **request.data.dict(),
                "user": request.user.id,
            },
            requester=request.user,
        )

        return Response(
            AppsViewCreateTRF(instance=app).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        result = self.apps_svc.retrieve(
            app_id=pk,
            requester=request.user,
        )

        return Response(
            AppsViewRetrieveTRF(instance=result).data,
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk):
        app = self.apps_svc.update(
            params=request.data,
            app_id=pk,
            requester=request.user,
        )

        return Response(
            AppsViewCreateTRF(instance=app).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        self.apps_svc.destroy(
            app_id=pk,
            requester=request.user,
        )

        return Response(status=status.HTTP_200_OK)
