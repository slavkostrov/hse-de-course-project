import datetime
from typing import Any

from modules.db.utils import provide_session
from modules.models import (
    DimAccount,
    DimCard,
    DimClient,
    DimTerminal,
    FactPassportBlacklist,
    FactTransaction,
)
from modules.models.report import FraudReport
from sqlalchemy import Date, and_, cast, func, or_
from sqlalchemy.orm import Session, aliased


def prepare_row(row, name: str) -> dict[str, Any]:
    """Подготавливает строчку для загрузки в отчет."""
    return {
        "event_dt": row.transaction_date,
        "passport": row.passport,
        "fio": f"{row.last_name} {row.first_name} {row.patronymic or ''}",
        "phone": row.phone,
        "event_type": name,
    }


def get_invalid_passport_transactions(session: Session, date: datetime.date) -> list[dict[str, Any]]:
    """Находит транзакции с паспортом, который находится в черном списке."""
    distinct_passports_subquery = session.query(FactPassportBlacklist.passport).distinct().subquery()

    FactPassportBlacklistDistinct = aliased(FactPassportBlacklist, distinct_passports_subquery)  # noqa

    query = (
        session.query(
            FactTransaction.date.label("transaction_date"),
            DimClient.passport_num.label("passport"),
            DimClient.last_name,
            DimClient.first_name,
            DimClient.patronymic,
            DimClient.phone,
        )
        .select_from(FactTransaction)
        .filter(cast(FactTransaction.date, Date) == date)
        .join(DimCard, FactTransaction.card_num == DimCard.card_num)
        .join(DimAccount, DimCard.account == DimAccount.account)
        .join(DimClient, DimAccount.client == DimClient.client_id)
        # джойним черный список
        # если запись будет
        .join(
            FactPassportBlacklistDistinct,
            DimClient.passport_num == FactPassportBlacklistDistinct.passport,
        )
    )

    return [prepare_row(row, name="passport_in_blacklist") for row in query]


def get_invalid_account_transactions(session: Session, date: datetime.date):
    """Находит транзакции с акаунтами, которые просрочились до момента транзакции."""
    query = (
        session.query(
            FactTransaction.date.label("transaction_date"),
            DimClient.passport_num.label("passport"),
            DimClient.last_name,
            DimClient.first_name,
            DimClient.patronymic,
            DimClient.phone,
        )
        .select_from(FactTransaction)
        .filter(cast(FactTransaction.date, Date) == date)
        .join(DimCard, FactTransaction.card_num == DimCard.card_num)
        .join(DimAccount, DimCard.account == DimAccount.account)
        .join(DimClient, DimAccount.client == DimClient.client_id)
        # если акаунт истек до дейттайма транзакции, то фрод
        .filter(DimAccount.valid_to < FactTransaction.date)
    )

    return [prepare_row(row, name="invalid_account") for row in query]


def get_cross_city_transactions(session: Session, date: datetime.date):
    """Находит транзакции с разбросом по городам."""
    subquery = (
        session.query(
            FactTransaction.date.label("transaction_date"),
            DimClient.passport_num.label("passport"),
            DimClient.last_name,
            DimClient.first_name,
            DimClient.patronymic,
            DimClient.phone,
            FactTransaction.terminal,
            DimTerminal.city,
            func.lag(DimTerminal.city)
            .over(partition_by=DimClient.client_id, order_by=FactTransaction.date)
            .label("previous_city"),
            func.lag(FactTransaction.date)
            .over(partition_by=DimClient.client_id, order_by=FactTransaction.date)
            .label("previous_dttm"),
            func.lead(DimTerminal.city)
            .over(partition_by=DimClient.client_id, order_by=FactTransaction.date)
            .label("next_city"),
            func.lead(FactTransaction.date)
            .over(partition_by=DimClient.client_id, order_by=FactTransaction.date)
            .label("next_dttm"),
        )
        .select_from(FactTransaction)
        .join(DimCard, FactTransaction.card_num == DimCard.card_num)
        .join(DimAccount, DimCard.account == DimAccount.account)
        .join(DimClient, DimAccount.client == DimClient.client_id)
        .join(DimTerminal, FactTransaction.terminal == DimTerminal.id)
        .subquery()
    )

    query = (
        session.query(
            subquery.c.transaction_date,
            subquery.c.passport,
            subquery.c.last_name,
            subquery.c.first_name,
            subquery.c.patronymic,
            subquery.c.phone,
            subquery.c.terminal,
        )
        .filter(
            or_(
                and_(
                    subquery.c.city != subquery.c.previous_city,
                    subquery.c.transaction_date - subquery.c.previous_dttm < datetime.timedelta(hours=1),
                ),
                and_(
                    subquery.c.city != subquery.c.next_city,
                    subquery.c.next_dttm - subquery.c.transaction_date < datetime.timedelta(hours=1),
                ),
            ),
        )
        .filter(cast(subquery.c.transaction_date, Date) == date)
    )

    return [prepare_row(row, name="different_city") for row in query]


def get_decreasing_amount_transactions(session: Session, date: datetime.date):
    """Находит транзакции с подозрительной последовательностью."""

    def client_lag(column, lag, name):
        return func.lag(column, lag).over(partition_by=DimClient.client_id, order_by=FactTransaction.date).label(name)

    subquery = (
        session.query(
            FactTransaction.date.label("transaction_date"),
            FactTransaction.card_num,
            FactTransaction.amount,
            FactTransaction.oper_result,
            DimClient.passport_num.label("passport"),
            DimClient.last_name,
            DimClient.first_name,
            DimClient.patronymic,
            DimClient.phone,
            client_lag(FactTransaction.oper_result, 1, "oper_result_lag_1"),
            client_lag(FactTransaction.oper_result, 2, "oper_result_lag_2"),
            client_lag(FactTransaction.amount, 1, "amount_lag_1"),
            client_lag(FactTransaction.amount, 2, "amount_lag_2"),
            client_lag(FactTransaction.date, 2, "period_start_dttm"),
        )
        .select_from(FactTransaction)
        .join(DimCard, FactTransaction.card_num == DimCard.card_num)
        .join(DimAccount, DimCard.account == DimAccount.account)
        .join(DimClient, DimAccount.client == DimClient.client_id)
        .subquery()
    )

    # TODO: тут не совсем понятно, но возможно правильней относить к фроду все, не только текущую запись
    query = (
        session.query(
            subquery.c.transaction_date,
            subquery.c.passport,
            subquery.c.last_name,
            subquery.c.first_name,
            subquery.c.patronymic,
            subquery.c.phone,
        )
        .filter(
            and_(
                subquery.c.amount < subquery.c.amount_lag_1,
                subquery.c.amount_lag_1 < subquery.c.amount_lag_2,
                subquery.c.transaction_date - subquery.c.period_start_dttm < datetime.timedelta(minutes=20),
                subquery.c.oper_result == "SUCCESS",
                subquery.c.oper_result_lag_1 == "REJECT",
                subquery.c.oper_result_lag_2 == "REJECT",
            ),
        )
        .filter(cast(subquery.c.transaction_date, Date) == date)
    )

    return [prepare_row(row, name="amount_transactins") for row in query]


def save_fraud_report(session, fraud_data):
    """Добавляет запись в таблицу с отчетом."""
    for data in fraud_data:
        report = FraudReport(
            event_dt=data.get("event_dt"),
            passport=data.get("passport"),
            fio=data.get("fio"),
            phone=data.get("phone"),
            event_type=data.get("event_type"),
        )
        session.add(report)


@provide_session
def generate_fraud_report(session: Session, date: datetime.date | str) -> None:
    """Генерирует отчет о фроде."""
    if date and isinstance(date, str):
        date = datetime.datetime.strptime(date, "%d-%m-%Y").date()  # noqa

    date = date or datetime.date.today()
    for report_func in (
        get_invalid_passport_transactions,
        get_invalid_account_transactions,
        get_cross_city_transactions,
        get_decreasing_amount_transactions,
    ):
        data = report_func(session, date=date)
        save_fraud_report(session, data)
