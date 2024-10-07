from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


UserModel: str = settings.AUTH_USER_MODEL


class YandexAccount(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    login = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250)

    first_name = models.CharField(max_length=250, blank=True, default="")
    last_name = models.CharField(max_length=250, blank=True, default="")

    avatar_id = models.CharField(max_length=250, default="0/0-0")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Yandex account")
        verbose_name_plural = _("Yandex accounts")
