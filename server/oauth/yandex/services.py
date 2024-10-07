from typing import Any
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from oauth.exceptions import OAuthAccessTokenError

from . import links, serializers
from .models import YandexAccount


UserModel = get_user_model()


def get_access_token(code: str) -> str:
    # response = requests.post(
    #     links.USER_INFO,
    #     data={
    #         "grant_type": "authorization_code",
    #         "code": code,
    #     },
    #     auth=HTTPBasicAuth(
    #         settings.YANDEX_CLIENT_ID,
    #         settings.YANDEX_CLIENT_SECRET,
    #     ),
    # )

    # if not response.ok:
    #     raise OAuthAccessTokenError()

    # data = response.json()

    data = {
        "access_token": "y0_AgAAAAA1xzpYAAyQUQAAAAETgEKTAACBkqD7kJFDMILOcbdLmcaq9oWevQ",
        "expires_in": 31535999,
        "refresh_token": "1:c2LrWqcq0WBh8LqE:0vsEUe2GG-dWT7aqTtObh-HXFXmpbHbhTepMYz1-BsRde1F1hX0dFnpBqhO4DB97W7q3q19vT9InUAsxCg:EaLvY0KpwzQPi09Gme0rhA",
        "token_type": "bearer",
    }

    if not isinstance(data, dict):
        raise ValueError(
            f"The response should be a `dict` instance, not `{type(data)}`",
        )

    if "access_token" not in data:
        raise ValueError(
            "The `access_token` field of the response data is required",
        )

    token = data["access_token"]

    return str(token)


def get_account_info(access_token: str) -> dict[str, Any]:
    # response = requests.get(
    #     links.USER_INFO,
    #     params={"format": "json"},
    #     headers={"Authorization": f"Bearer {access_token}"},
    # )

    serializer = serializers.IncomingYandexAccountSerializer(
        # data=response.json()
        data={
            "id": "902249048",
            "login": "drsilvana",
            "client_id": "90b6b59aee8b4aeb8497ad96a01235a2",
            "display_name": "Артём Япрынцев",
            "real_name": "Артём Япрынцев",
            "first_name": "Артём",
            "last_name": "Япрынцев",
            "sex": "male",
            "default_email": "drsilvana@yandex.ru",
            "emails": ["drsilvana@yandex.ru"],
            "birthday": "2002-06-14",
            "default_avatar_id": "0/0-0",
            "is_avatar_empty": True,
            "psuid": "1.AAyQUQ.RwJktOPoi9hmjoxzfxc81g.xyMAstisU1rZKmptifzzTw",
        }
    )

    if not isinstance(serializer, serializers.IncomingYandexAccountSerializer):
        raise ValueError(
            "The received user data should be a dictionary instance only, "
            "not list or another",
        )

    if not serializer.is_valid():
        raise ValueError(
            "Received invalid user data, error: %s" % serializer.errors,
        )

    return serializer.validated_data  # type: ignore


def proceed_yandex_user_info(
    user_info: serializers.IncomingYandexAccountSerializer,
) -> AbstractUser:
    ya_account = YandexAccount(**user_info.data)

    if YandexAccount.objects.filter(id=ya_account.id).exists():
        user = ya_account.user

        if not user:
            raise ValueError(
                f"The `YandexAccount` model instance with `{ya_account.id}` "
                "does not related with user",
            )

        return ya_account.user

    user, is_created = user

    # return UserModel()
