from django.db import models
from apps.acсount.models import User


class UserSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    refresh_token = models.CharField(
        editable=False,
        unique=True,
    )
    expires_in = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return f'{self.user.username} - {self.refresh_token}'