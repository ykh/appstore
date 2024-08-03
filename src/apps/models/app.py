import uuid

from django.contrib.auth import get_user_model
from django.db import models


class App(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def verify(self):
        self.is_verified = True
        self.save(update_fields=['is_verified'])

    def activate(self):
        self.is_activated = True
        self.save(update_fields=['is_activated'])

    def __str__(self):
        return f'{self.title}'

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['user']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['is_activated']),
        ]
