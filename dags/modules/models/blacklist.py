import datetime

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DATE, Column, String

from modules.models.base import Base, DeclarativeBase


class BlacklistModel(BaseModel):
    """Модель для валидации входящих полей."""

    model_config = ConfigDict(from_attributes=True)
    date: datetime.date = Field()
    passport: str = Field(min_length=11, max_length=11)


class StagingPassportBlacklist(DeclarativeBase, Base):
    """Таблица с данными о черном списке паспортов, пример данных:

    date	    passport
    2021-03-01	9933 106914
    """

    __custom_table_name__ = "stg_blacklist"

    # https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#how-do-i-map-a-table-that-has-no-primary-key
    date = Column(DATE, nullable=False, primary_key=True, comment="Дата актуальности данных")
    passport = Column(String(length=11), nullable=False, primary_key=True, comment="Серия и номер паспорта")


class FactPassportBlacklist(DeclarativeBase, Base):
    """Паспорт с фактической информацией о паспортах."""

    __custom_table_name__ = "fact_passport_blacklist"

    date = Column(DATE, nullable=False, primary_key=True, comment="Дата актуальности данных")
    passport = Column(String(length=11), nullable=False, primary_key=True, comment="Серия и номер паспорта")
