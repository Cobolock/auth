from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from redis.asyncio import Redis

from auth.core.exceptions import (
    BadRefreshTokenError,
    NotAuthorizedError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from auth.db.redis import get_redis
from auth.schemas.user import Entry as EntrySchema
from auth.models.user import User
from auth.models.entry import Entry as EntryModel
from auth.repositories.entry import EntryRepository
from auth.repositories.role import RoleRepository
from auth.repositories.user import UserRepository
from auth.schemas.user import Credentials
from auth.services.jwt import JWTPair, JWTService


@dataclass
class UserService:
    user_repo: Annotated[UserRepository, Depends()]
    role_repo: Annotated[RoleRepository, Depends()]
    entry_repo: Annotated[EntryRepository, Depends()]
    cache_session: Annotated[Redis, Depends(get_redis)]
    jwt_service: Annotated[JWTService, Depends()]

    async def create_user(self, creds: Credentials) -> bool:
        new_user = User(creds.username, creds.password)
        try:
            await self.user_repo.add(new_user)
        except ObjectAlreadyExistsError:
            return False
        return True

    async def check_creds(self, creds: Credentials) -> bool:
        if user := await self.user_repo.get_by_username_or_none(creds.username):
            return user.check_password(creds.password)
        return False

    async def change_auth(self, username: str, creds: Credentials) -> None:
        if user := await self.user_repo.get_by_username_or_none(username):
            if creds.username != "":
                user.username = creds.username
            if creds.password != "":
                user.password = user.make_password(creds.password)
            await self.user_repo.update(user)
            await self.revoke_all_tokens(username)

    async def refresh(self, refresh_token) -> JWTPair:
        username = await self.jwt_service.get_sub(refresh_token)
        if await self.revoke_token(username, refresh_token):
            jwt = await self.jwt_service.generate(subject=username)
            await self.cache_token(username, jwt.RT)
        else:
            raise BadRefreshTokenError
        return jwt

    async def login(self, creds: Credentials) -> JWTPair:
        if await self.check_creds(creds):
            jwt = await self.jwt_service.generate(subject=creds.username)
            await self.cache_token(creds.username, jwt.RT)
            return jwt
        raise NotAuthorizedError from None

    async def logout(self, refresh_token: str) -> bool:
        if username := await self.jwt_service.get_sub(refresh_token):
            return await self.revoke_token(username, refresh_token)
        raise ObjectNotFoundError(User) from None

    async def revoke_token(self, username, refresh_token) -> bool:
        if await self.cache_session.sismember(f"user:{username}", refresh_token):
            await self.cache_session.srem(f"user:{username}", refresh_token)
        else:
            raise BadRefreshTokenError
        return True

    async def revoke_all_tokens(self, username) -> None:
        await self.cache_session.delete(f"user:{username}")

    async def cache_token(self, username, token) -> None:
        await self.cache_session.sadd(f"user:{username}", token)

    async def add_role(self, username: str, role_id: str) -> User:
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        user.roles.add(role)
        return await self.user_repo.update(user)

    async def remove_role(self, username: str, role_id: str) -> User:
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        if role in user.roles:
            user.roles.remove(role)
        return await self.user_repo.update(user)

    async def add_entry(self, username: str, entry: EntrySchema) -> None:
        user = await self.user_repo.get_by_username(username)
        entry.user_id = user.id
        new_entry = EntryModel(**entry.model_dump())
        await self.entry_repo.add(new_entry)

    async def get_entries(self, username: str) -> list[EntryModel]:
        user = await self.user_repo.get_by_username(username)
        return await self.entry_repo.get_all(user.id)
