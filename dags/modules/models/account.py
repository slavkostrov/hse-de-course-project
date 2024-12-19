import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String

from modules.models.base import Base, DeclarativeBase


class AccountModel(BaseModel):
    """Модель для валидации входящих полей для сущности Аккаунт."""

    account: str = Field(..., description="Номер счета клиента")
    valid_to: datetime.date = Field(..., description="Дата, до которой данные действительны")
    client: int = Field(..., description="Идентификатор клиента")
    create_dt: datetime.datetime = Field(..., description="Дата создания записи")
    update_dt: datetime.datetime = Field(None, description="Дата последнего обновления записи")


class StagingAccount(DeclarativeBase, Base):
    """Таблица с данными об аккаунтах, пример данных:

    account                valid_to    client    create_dt    update_dt
    40817810263651414075    2022-01-15    6948    1900-01-01    None
    """

    __custom_table_name__ = "stg_accounts"

    account = Column(String, primary_key=True)
    valid_to = Column(DateTime, nullable=False)
    client = Column(Integer, nullable=False)
    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)
