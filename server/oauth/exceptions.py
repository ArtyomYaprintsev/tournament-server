from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class OAuthAccessTokenError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _(
        "Can not to fetch the access token with the received code, try again "
        "later",
    )
