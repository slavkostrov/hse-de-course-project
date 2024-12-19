from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, String, func

from modules.models.base import Base, DeclarativeBase


class TerminalModel(BaseModel):
    """Модель для валидации входящих полей для сущности Терминал."""

    id: str = Field(max_length=10, alias="terminal_id")
    type: Literal["ATM", "POS"] = Field(alias="terminal_type")
    city: str = Field(max_length=100, alias="terminal_city")
    address: str = Field(max_length=255, alias="terminal_address")


class StagingTerminal(DeclarativeBase, Base):
    """Таблица с данными о терминалах, пример данных:

    terminal_id	terminal_type	terminal_city   terminal_address
    A1096	    ATM	            Кемерово	    г. Кемерово, 1-й Электрозаводский пер., д. 3
    """

    __custom_table_name__ = "stg_terminals"

    id = Column(String(10), primary_key=True, nullable=False, comment="Идентификатор терминала")
    type = Column(String(50), nullable=False, comment="Тип терминала")
    city = Column(String(100), nullable=False, comment="Город расположения терминала")
    address = Column(String(255), nullable=False, comment="Адрес терминала")


class DimTerminal(DeclarativeBase, Base):
    """Таблица с информацией о терминалах."""

    __custom_table_name__ = "dwh_dim_terminals"

    id = Column(String(10), primary_key=True, nullable=False, comment="Идентификатор терминала")
    type = Column(String(50), nullable=False, comment="Тип терминала")
    city = Column(String(100), nullable=False, comment="Город расположения терминала")
    address = Column(String(255), nullable=False, comment="Адрес терминала")

    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)


class DimTerminalHist(DeclarativeBase, Base):
    """Историческая таблица с информцией о терминалах."""

    __custom_table_name__ = "dwh_dim_terminals_hist"

    id = Column(String(10), primary_key=True, nullable=False, comment="Идентификатор терминала")
    type = Column(String(50), nullable=False, comment="Тип терминала")
    city = Column(String(100), nullable=False, comment="Город расположения терминала")
    address = Column(String(255), nullable=False, comment="Адрес терминала")

    effective_from = Column(DateTime, default=func.current_date(), primary_key=True)
    effective_to = Column(DateTime, nullable=True)
    deleted_flg = Column(Boolean, nullable=False)
