from typing import Annotated, Any

from dataclasses import dataclass

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from async_fastapi_jwt_auth.exceptions import JWTDecodeError
from fastapi import Depends

from auth.core.config import jwt_settings
from auth.core.exceptions import BadRefreshTokenError, TokenMalformedError

get_jwt = AuthJWTBearer()


@AuthJWT.load_config
def get_config():
    return jwt_settings


@dataclass
class JWTPair:
    AT: str
    RT: str

    def format(self) -> dict:
        return {"access_token": self.AT, "refresh_token": self.RT}


class JWTService:
    def __init__(self, jwt: Annotated[AuthJWT, Depends(get_jwt)]) -> None:
        self._jwt = jwt
        self.AT: str
        self.RT: str

    async def generate(self, subject: str, user_claims: dict[str, Any] | None = None) -> JWTPair:
        self.AT = await self._jwt.create_access_token(
            subject=subject, user_claims=user_claims or {}
        )
        self.RT = await self._jwt.create_refresh_token(subject=subject)
        return JWTPair(self.AT, self.RT)

    async def get_payload(self, refresh_token: str) -> dict[str, Any]:
        try:
            return await self._jwt.get_raw_jwt(refresh_token)
        except JWTDecodeError:
            raise JWTDecodeError from None
        except ValueError:
            raise TokenMalformedError from None

    async def get_sub(self, refresh_token: str) -> str:
        try:
            payload = await self.get_payload(refresh_token)
        except JWTDecodeError:
            raise BadRefreshTokenError from None

        return payload["sub"]
