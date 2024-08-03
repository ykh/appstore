from django.contrib.auth.models import (
    BaseUserManager,
)


class PurchaseManager(BaseUserManager):
    def is_app_already_purchased_by_user(self, app_id: str, user_id: str) -> bool:
        return self.filter(app_id=app_id, user_id=user_id).exists()
