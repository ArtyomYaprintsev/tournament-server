import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class UserSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    fingerprint = models.CharField(max_length=255,)
    refresh_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    expires_in = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return f'{self.user.username} - {self.refresh_token}'