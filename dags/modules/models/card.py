import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from modules.models.base import TABLE_PREFIX, Base, DeclarativeBase


class CardModel(BaseModel):
    """Модель для валидации входящих полей для сущности Карта."""

    card_num: str = Field()
    account: str = Field()
    create_dt: datetime.datetime = Field()
    update_dt: datetime.datetime | None = Field()


class StagingCard(DeclarativeBase, Base):
    """Таблица с данными о картах, пример данных:

    card_num	        account	                create_dt	update_dt
    2714 8073 9433 4375	40817810437543724522	2001-01-01	None
    """

    __custom_table_name__ = "stg_cards"

    card_num = Column(String(19), primary_key=True, nullable=False)
    account = Column(String(22), nullable=False)


class DimCard(DeclarativeBase, Base):
    """Таблица с данными о картах."""

    __custom_table_name__ = "dwh_dim_cards"

    card_num = Column(String(19), nullable=False, primary_key=True, unique=True)
    account = Column(String(22), ForeignKey(f"{TABLE_PREFIX}_dwh_dim_accounts.account"), nullable=False)
    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)

    card_account = relationship("DimAccount", back_populates="cards")


class DimCardHist(DeclarativeBase, Base):
    """Таблица с историческими данными о картах."""

    __custom_table_name__ = "dwh_dim_cards_hist"

    card_num = Column(String(19), primary_key=True, nullable=False)
    account = Column(String(22), nullable=False)
    effective_from = Column(DateTime, default=func.current_date(), primary_key=True)
    effective_to = Column(DateTime, nullable=True)
    deleted_flg = Column(Boolean, nullable=False)
