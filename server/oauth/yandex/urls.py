from django.urls import path

from . import views


urlpatterns = [
    path("uri/", views.get_yandex_oauth_uri, name="yandex-auth-uri"),
    path("auth/", views.login_with_yandex_account, name="yandex-auth"),
    path("link/", views.link_user_with_yandex_account, name="yandex-link"),
]
