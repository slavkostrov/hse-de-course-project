import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from modules.models.base import Base, DeclarativeBase


class ClientModel(BaseModel):
    """Модель для валидации входящих полей для сущности Клиент."""

    client_id: str = Field()
    last_name: str = Field()
    first_name: str = Field()
    patronymic: str = Field()
    date_of_birth: datetime.date = Field()
    passport_num: str = Field()
    passport_valid_to: datetime.date | None = Field()
    phone: str = Field()
    create_dt: datetime.datetime = Field()
    update_dt: datetime.datetime | None = Field()


class StagingClient(DeclarativeBase, Base):
    """Таблица с данными о клиентах, пример данных:

    client_id	last_name	first_name	patronymic	    date_of_birth	passport_num	passport_valid_to
    6948	    Сьестнов	Сергей	    Станиславович	1973-04-05	    8732 868620	    None

    phone               create_dt	update_dt
    +7 914 996-22-46    1900-01-01	None
    """

    __custom_table_name__ = "stg_clients"

    client_id = Column(String, primary_key=True, nullable=False)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    passport_num = Column(String(20), nullable=False)
    passport_valid_to = Column(DateTime, nullable=True)
    phone = Column(String(20), nullable=False)


class DimClient(DeclarativeBase, Base):
    """Таблица с данными о клиентах."""

    __custom_table_name__ = "dwh_dim_clients"

    client_id = Column(String, primary_key=True, nullable=False)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    passport_num = Column(String(20), nullable=False)
    passport_valid_to = Column(DateTime, nullable=True)
    phone = Column(String(20), nullable=False)
    create_dt = Column(DateTime, nullable=False)
    update_dt = Column(DateTime, nullable=True)

    accounts = relationship("DimAccount", back_populates="client_details")


class DimClientHist(DeclarativeBase, Base):
    """Таблица с историческими данными о клиентах."""

    __custom_table_name__ = "dwh_dim_clients_hist"

    client_id = Column(String, primary_key=True, nullable=False)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    passport_num = Column(String(20), nullable=False)
    passport_valid_to = Column(DateTime, nullable=True)
    phone = Column(String(20), nullable=False)

    effective_from = Column(DateTime, default=func.current_date(), primary_key=True)
    effective_to = Column(DateTime, nullable=True)
    deleted_flg = Column(Boolean, nullable=False)
