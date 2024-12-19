import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String

from modules.models.base import Base, DeclarativeBase


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_num = Column(String(19), nullable=False)
    account = Column(String(22), nullable=False)
    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)
