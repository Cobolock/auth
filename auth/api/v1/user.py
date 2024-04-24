from typing import Annotated

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from auth.schemas.user import Credentials
from auth.schemas.user import Entry as EntrySchema
from auth.models.entry import Entry as EntryModel
from auth.services.user import UserService

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def new_user(
    credentials: Credentials, user_service: Annotated[UserService, Depends()]
) -> dict:
    status = await user_service.create_user(credentials)
    if status:
        return {"detail": "Created"}
    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Username in use")


@router.post("/login", status_code=HTTPStatus.OK)
async def user_login(
    credentials: Credentials, user_service: Annotated[UserService, Depends()]
) -> dict:
    """Проверить логин и пароль, выдать в ответ JWT."""
    jwt = await user_service.login(credentials)
    return jwt.format()


@router.post("/refresh", status_code=HTTPStatus.OK)
async def user_refresh(refresh_token: str, user_service: Annotated[UserService, Depends()]) -> dict:
    """Обновить Refresh Token, если он валидный."""
    jwt = await user_service.refresh(refresh_token)
    return jwt.format()


@router.post("/logout", status_code=HTTPStatus.OK)
async def user_logout(refresh_token: str, user_service: Annotated[UserService, Depends()]) -> None:
    """Удаляет RT из кэша."""
    await user_service.logout(refresh_token)


@router.post("/entry", status_code=HTTPStatus.OK)
async def add_entry(
    username: str, entry: EntrySchema, user_service: Annotated[UserService, Depends()]
) -> None:
    """Вносит запись о входе пользователя."""
    await user_service.add_entry(username, entry)


@router.get("/entries", status_code=HTTPStatus.OK, response_model=list[EntrySchema])
async def get_entries(
    username: str, user_service: Annotated[UserService, Depends()]
) -> list[EntryModel]:
    """Выводит все записи о входах пользователя."""
    return await user_service.get_entries(username)
