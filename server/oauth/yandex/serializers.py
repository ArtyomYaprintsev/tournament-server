from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import YandexAccount


UserModel = get_user_model()


class BaseYandexAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = YandexAccount
        fields = [
            "id",
            "login",
            "email",
            "first_name",
            "last_name",
            "avatar_id",
        ]


class IncomingYandexAccountSerializer(BaseYandexAccountSerializer):
    FIELD_ALIASES = {
        "avatar_id": "default_avatar_id",
        "email": "default_email",
    }

    def to_internal_value(self, data: dict):
        for field, field_alias in self.FIELD_ALIASES.items():
            data[field] = data.get(field_alias)

        return super().to_internal_value(data)


class YandexAccountToUserSerializer(serializers.ModelSerializer):
    pass
