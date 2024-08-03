from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.services.serializers.signup_srl import UsersSVCSignUpVLD
from users.services.users_svc import UsersService
from users.views.serializers.signup_srl import UsersViewSignUpTRF, UsersViewSignUpVLD


class UsersViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.users_svc = UsersService()

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        request_vld = UsersViewSignUpVLD(data=request.data)
        request_vld.is_valid(raise_exception=True)
        params = request_vld.validated_data

        result = self.users_svc.signup(
            params=UsersSVCSignUpVLD(data=params),
        )

        return Response(
            UsersViewSignUpTRF(result).data,
            status=status.HTTP_201_CREATED
        )
