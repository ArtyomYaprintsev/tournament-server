# Oauth module

## Yandex

### Flow

1. Redirect user to:

    ```txt
    https://oauth.yandex.ru/authorize?response_type=code
    & client_id=<идентификатор приложения>
    [& device_id=<идентификатор устройства>]
    [& device_name=<имя устройства>]
    [& redirect_uri=<адрес перенаправления>]
    [& login_hint=<имя пользователя или электронный адрес>]
    [& scope=<запрашиваемые необходимые права>]
    [& optional_scope=<запрашиваемые опциональные права>]
    [& force_confirm=yes]
    [& state=<произвольная строка>]
    [& code_challenge=<преобразованная верcия верификатора code_verifier>]
    [& code_challenge_method=<метод преобразования>]
    ```

    Source: https://yandex.ru/dev/id/doc/en/codes/code-url#code

2. Receive request with confirmation code

3. Exchanging a confirmation code for an OAuth token
