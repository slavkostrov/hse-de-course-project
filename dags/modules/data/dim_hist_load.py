import logging
from collections.abc import Sequence

from modules.data.source import DEFAULT_SOURCE_LIST, DimSource, Source
from modules.db.utils import provide_session
from sqlalchemy import func, inspect
from sqlalchemy.orm import Session


def _load_to_dim_hist(session: Session, dim_source: DimSource) -> None:
    logging.info("loading into dim hist table: %s", dim_source)
    dim_table = dim_source.dim_table
    dim_hist_table = dim_source.dim_hist_table

    inspected_table = inspect(dim_table)
    primary_key, *cols = inspected_table.primary_key
    columns = [column.name for column in inspected_table.columns]

    if len(cols) > 0:
        raise RuntimeError(f"more than 1 pk: {cols}")

    primary_key = primary_key.name
    dim_data = session.query(dim_table).all()

    for record in dim_data:
        existing_hist = (
            session.query(dim_hist_table)
            .filter(
                getattr(dim_hist_table, primary_key) == getattr(record, primary_key),
                dim_hist_table.effective_to == None,
            )
            .first()
        )

        if existing_hist and all(
            getattr(record, column) == getattr(existing_hist, column)
            for column in columns
            if column not in ("create_dt", "update_dt")
        ):
            continue

        historical_record = dim_hist_table(
            **{column: getattr(record, column) for column in columns if column not in ("create_dt", "update_dt")},
            effective_from=func.current_timestamp(),
            effective_to=None,
            deleted_flg=False,
        )

        session.add(historical_record)

        if existing_hist:
            existing_hist.effective_to = func.current_timestamp()
            existing_hist.deleted_flg = True


@provide_session
def load_to_dim_hist(session: Session, source_list: Sequence[Source] = DEFAULT_SOURCE_LIST) -> None:
    """Загружает данные в dim_hist таблицы."""
    dim_source_list = list(filter(lambda source: isinstance(source, DimSource), source_list))
    for dim_source in dim_source_list:
        _load_to_dim_hist(session=session, dim_source=dim_source)
