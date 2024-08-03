from appstore.utils.singleton import singleton
from users.models import User
from users.services.serializers.signup_srl import UsersSVCSignUpVLD


@singleton
class UsersService:
    def signup(self, params: UsersSVCSignUpVLD) -> User:
        params.is_valid(raise_exception=True)
        user = params.save()

        return user
