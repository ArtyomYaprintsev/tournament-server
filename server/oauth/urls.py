from django.urls import path, include


urlpatterns = [
    path("yandex/", include("oauth.yandex.urls")),
]
