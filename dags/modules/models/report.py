from sqlalchemy import Column, Date, String, func

from modules.models.base import Base, DeclarativeBase


class FraudReport(DeclarativeBase, Base):
    """Отчет от фроде в транзакциях."""

    __custom_table_name__ = "rep_fraud"

    event_dt = Column(Date, primary_key=True, nullable=False)
    passport = Column(String(20), nullable=False)
    fio = Column(String, nullable=False)
    phone = Column(String(20), nullable=True)
    event_type = Column(String, nullable=False)
    report_dt = Column(Date, nullable=False, default=func.current_date())
