import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from modules.models.base import TABLE_PREFIX, Base, DeclarativeBase


class AccountModel(BaseModel):
    """Модель для валидации входящих полей для сущности Аккаунт."""

    account: str = Field()
    valid_to: datetime.date = Field()
    client: str = Field()
    create_dt: datetime.datetime = Field()
    update_dt: datetime.datetime | None = Field()


class StagingAccount(DeclarativeBase, Base):
    """Таблица с данными об аккаунтах, пример данных:

    account                valid_to    client    create_dt    update_dt
    40817810263651414075    2022-01-15    6948    1900-01-01    None
    """

    __custom_table_name__ = "stg_accounts"

    account = Column(String, primary_key=True)
    valid_to = Column(DateTime, nullable=False)
    client = Column(String, nullable=False)


class DimAccount(DeclarativeBase, Base):
    """Таблица с данными об аккаунтах."""

    __custom_table_name__ = "dwh_dim_accounts"

    account = Column(String, primary_key=True, unique=True)
    valid_to = Column(DateTime, nullable=False)
    client = Column(String, ForeignKey(f"{TABLE_PREFIX}_dwh_dim_clients.client_id"), nullable=False)
    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)

    cards = relationship("DimCard", back_populates="card_account")
    client_details = relationship("DimClient", back_populates="accounts")


class DimAccountHist(DeclarativeBase, Base):
    """Таблица с историческими данными об аккаунтах."""

    __custom_table_name__ = "dwh_dim_accounts_hist"

    account = Column(String, primary_key=True)
    valid_to = Column(DateTime, nullable=False)
    client = Column(String, nullable=False)

    effective_from = Column(DateTime, default=func.current_date(), primary_key=True)
    effective_to = Column(DateTime, nullable=True)
    deleted_flg = Column(Boolean, nullable=False)
