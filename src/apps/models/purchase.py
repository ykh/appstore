import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.models import App
from apps.models.managers.purchase_manager import PurchaseManager


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    app_link = models.URLField(max_length=200)
    purchased_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PurchaseManager()

    def __str__(self):
        return (
            f'{self.user} '
            f'purchased {self.app} for {self.cost} on {self.purchased_at}'
        )

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['app']),
        ]
