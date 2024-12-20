import logging
from collections.abc import Sequence

from modules.data.source import DEFAULT_SOURCE_LIST, FactSource, Source
from modules.db.utils import provide_session
from sqlalchemy.orm import Session


def _load_fact(session: Session, fact_source: FactSource) -> None:
    logging.info("loading into fact table: %s", fact_source)
    query = session.query(fact_source.target_table)
    data_to_insert = [
        {column.name: getattr(row, column.name) for column in fact_source.target_table.__table__.columns}
        for row in query.all()
    ]
    session.bulk_insert_mappings(fact_source.fact_table, data_to_insert)


@provide_session
def load_fact_data(session: Session, source_list: Sequence[Source] = DEFAULT_SOURCE_LIST):
    """Загружает данные в таблицу с фактами."""
    fact_source_list = list(filter(lambda source: isinstance(source, FactSource), source_list))
    for fact_source in fact_source_list:
        _load_fact(session, fact_source)
