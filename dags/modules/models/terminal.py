from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import Column, String

from modules.models.base import Base, DeclarativeBase


class TerminalModel(BaseModel):
    """Модель для валидации входящих полей для сущности Терминал."""

    id: str = Field(max_length=10)
    type: Literal["ATM", "POS"] = Field()
    city: str = Field(max_length=100)
    address: str = Field(max_length=255)


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
