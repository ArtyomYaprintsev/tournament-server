from urllib import parse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from oauth.utils import get_state

from . import links, services
from .models import YandexAccount


UserModel = get_user_model()


@api_view(["GET"])
def get_yandex_oauth_uri(request: Request):
    print(
        request.query_params,
        request.data,
        request.query_params.get("redirect_uri"),
    )

    query_params = {
        "response_type": "code",
        "client_id": settings.YANDEX_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/oauth/yandex/",
        "force_confirm": 1,
        "state": get_state(),
    }

    return Response(
        {"uri": links.AUTH + "?" + parse.urlencode(query_params)},
    )


@api_view(["POST"])
def login_with_yandex_account(request: Request):
    print(
        request.query_params,
        request.query_params.get("code"),
        request.query_params.get("state"),
        request.query_params.get("cid"),
    )

    code = request.query_params.get("code")

    if not isinstance(code, str) and not code:
        raise ValueError("Code should be a non-empty string")

    access_token = services.get_access_token(code)
    user_data = services.get_account_info(access_token)

    # if not YandexAccount.objects.filter(id=user_data.get("id")).exists():
    #     email = user_data.get("email")

    #     user, _ = UserModel.objects.get_or_create(
    #         email=email,
    #         defaults={
    #             "username": user_data.get("login"),
    #             "email": email,
    #             "first_name": user_data.get("first_name"),
    #             "last_name": user_data.get("last_name"),
    #             # avatar proceed
    #         },
    #     )

    #     ya_account = YandexAccount.objects.create(**user_data, user_id=user.pk)
    # else:
    #     # user = UserModel.objects.get(user.yandexaccount_set.filter())
    #     # ya_account = YandexAccount.objects.get(id=user_data.get("id"))
    #     # user = ya_account.user
    #     pass

    print(user_data)
    return Response(user_data)


@api_view(["POST"])
def link_user_with_yandex_account():
    pass
