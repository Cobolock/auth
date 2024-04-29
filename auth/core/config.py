import sys

from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """Настройки PostgreSQL."""

    model_config = SettingsConfigDict(extra="ignore")

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    user: SecretStr = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field("auth_db", alias="POSTGRES_DB")
    host: str = Field("127.0.0.1", alias="POSTGRES_HOST")
    port: int = Field(5432, alias="POSTGRES_PORT")

    @property
    def dsn(self) -> str:
        return (
            f"{self.dialect}+{self.driver}://{self.user.get_secret_value()}:"
            f"{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
        )


class RedisConfig(BaseSettings):
    """Настройки Redis."""

    model_config = SettingsConfigDict(extra="ignore")

    host: str = Field("127.0.0.1", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")


class ExtraConfig(BaseSettings):
    """Прочие настройки."""

    model_config = SettingsConfigDict(extra="ignore")

    salt: str = Field(..., alias="SALT")


class JWTSettings(BaseSettings):
    """Параметры конфигурации JWT."""

    model_config = SettingsConfigDict(extra="ignore")

    authjwt_secret_key: str = Field(..., alias="JWT_SECRET")


env_path = Path(__file__).parent.parent.parent / "envs"
env_filename = ".env.test" if "pytest" in sys.modules else ".env"
env_file = env_path / env_filename

pg_config = PostgresConfig(_env_file=env_file)
redis_config = RedisConfig(_env_file=env_file)
extra_config = ExtraConfig(_env_file=env_file)
jwt_settings = JWTSettings(_env_file=env_file)
