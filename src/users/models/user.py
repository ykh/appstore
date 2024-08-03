import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models.managers.user_manager import UserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['credit']),
        ]
