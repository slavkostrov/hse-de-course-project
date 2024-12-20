import datetime
from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, ForeignKey, String

from modules.models.base import TABLE_PREFIX, Base, DeclarativeBase


class TransactionModel(BaseModel):
    """Модель для валидации входящих полей для сущности Транзакция."""

    id: int = Field(alias="transaction_id")
    date: datetime.datetime = Field(alias="transaction_date")
    amount: float = Field(gt=0)
    card_num: str = Field(pattern=r"^\d{4}( \d{4}){3}$")
    oper_type: Literal["PAYMENT", "WITHDRAW", "DEPOSIT"] = Field()
    oper_result: Literal["SUCCESS", "REJECT"] = Field()
    terminal: str = Field()


class StagingTransaction(DeclarativeBase, Base):
    """Таблица с данными о транзакциях, пример данных.

    transaction_id	transaction_date	amount	card_num	        oper_type	oper_result	terminal
    43845789347	    2021-03-01 00:00:01	1046,40	4513 5880 2369 1799	PAYMENT	    SUCCESS	    P5456
    """

    __custom_table_name__ = "stg_transactions"

    id = Column(String, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    card_num = Column(String, nullable=False)
    oper_type = Column(String, nullable=False)
    oper_result = Column(String, nullable=False)
    terminal = Column(String, nullable=False)


class FactTransaction(DeclarativeBase, Base):
    """Таблица с фактическими транзакциями."""

    __custom_table_name__ = "dwh_fact_transactions"

    id = Column(String, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    card_num = Column(String, ForeignKey(f"{TABLE_PREFIX}_dwh_dim_cards.card_num"), nullable=False)
    oper_type = Column(String, nullable=False)
    oper_result = Column(String, nullable=False)
    terminal = Column(String, ForeignKey(f"{TABLE_PREFIX}_dwh_dim_terminals.id"), nullable=False)
