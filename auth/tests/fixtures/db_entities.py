import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.models.role import Role
from auth.models.user import User


@pytest.fixture()
async def role_in_db(session: AsyncSession) -> Role:
    role = Role(id="moderator", name="Модератор", permissions=[])
    session.add(role)
    await session.commit()
    return role


@pytest.fixture()
async def roles_in_db(session: AsyncSession) -> list[Role]:
    roles = [
        Role(id="moderator", name="Модератор", permissions=[]),
        Role(id="user", name="Пользователь", permissions=[]),
    ]
    session.add_all(roles)
    await session.commit()
    return roles


@pytest.fixture()
async def admin_role_in_db(session: AsyncSession) -> Role:
    return await session.get_one(Role, "admin", options=[selectinload(Role.permissions)])


@pytest.fixture()
async def user_in_db(session: AsyncSession) -> User:
    user = User(username="user", password="password")  # noqa: S106
    session.add(user)
    await session.commit()
    return user
