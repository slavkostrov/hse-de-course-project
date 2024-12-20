import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """Настройки подключения к БД."""

    host: SecretStr
    port: int
    user: SecretStr
    password: SecretStr
    database: str
    verbose: bool = False

    class Config:
        """Конфиг для настроек."""

        env_file = f"{os.environ.get('AIRFLOW_HOME', '../..')}/.env"


db_settings = PostgresSettings()
