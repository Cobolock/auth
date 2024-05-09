"""Описание работы OAuth.

Для проверки работы OAuth следует использовать эндпоинт
"http://localhost:8000/api/v1/user/login/yandex/" открытый во вкладке браузера
в Приложении Яндекс ID указать Redirect URI
"https://tolocalhost.com/api/v1/user/login/yandex/redirect" который возвращает
код авторизации на "http://localhost:8000/api/v1/user/login/yandex/redidrect"
после чего, с помощью этого кода получаем токены доступа от Яндекс ID
передавая его  на "https://oauth.yandex.ru/token". Взамен получаем токена
доступа и передавая их на "https://login.yandex.ru/info", получаем информацию
о пользователе, которую в дальнейшем используем для создания его модели в БД и
выдаче для него JWT-токенов для последующей авторизации на Auth-сервисе
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from auth.core.config import yandex_auth_settings
from auth.core.utils import generate_random_string
from auth.schemas.user_auth import UserCredentials
from auth.services.oauth import YandexService
from auth.services.user import UserService

router = APIRouter()


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Войти с помощью Yandex OAuth",
    description="Переадресация запроса на Яндекс ID с целью подтверждения"
    " клиентом кода авторизации",
)
async def provider_login(request: Request) -> RedirectResponse:
    state = generate_random_string()
    request.session["state"] = state
    url = (
        f"https://oauth.yandex.ru/authorize"
        f"?response_type=code"
        f"&client_id={yandex_auth_settings.yandex_client_id}"
        f"&redirect_uri={yandex_auth_settings.yandex_redirect_uri}"
        f"&state={state}"
    )
    return RedirectResponse(url)


@router.get(
    "/login/yandex/redirect",
    status_code=status.HTTP_201_CREATED,
    summary="Получить токены с помощью Yandex OAuth",
    description="Переадресация запроса на Яндекс ID с целью подтверждения"
    "клиентом кода авторизации",
)
async def yandex_login_redirect(
    code: str,
    state: str,
    request: Request,
    user_service: Annotated[UserService, Depends()],
    yandex_service: Annotated[YandexService, Depends()],
) -> dict:
    if state != request.session["state"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="State check failed")
    user = await yandex_service.get_user(code)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Confirm code error")
    credentials = UserCredentials(username=user.username, password=user.password)
    jwt = await user_service.login(credentials)
    return jwt.format()