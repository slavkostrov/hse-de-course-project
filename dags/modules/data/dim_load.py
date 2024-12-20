import logging
from collections.abc import Sequence

from modules.data.source import DEFAULT_SOURCE_LIST, DimSource, Source
from modules.db.utils import provide_session
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session


def _load_to_dim(session: Session, dim_source: DimSource) -> None:
    logging.info("loading into dim table: %s", dim_source)
    staging_table = dim_source.target_table
    dim_table = dim_source.dim_table

    inspected_table = inspect(staging_table)
    primary_key, *cols = inspected_table.primary_key
    columns = [column.name for column in inspected_table.columns]

    if len(cols) > 0:
        raise RuntimeError(f"more than 1 pk: {cols}")

    primary_key = primary_key.name

    # TODO: fix, all in memory
    staging_data = session.query(staging_table).all()

    for record in staging_data:
        existing_record = (
            session.query(dim_table).filter(getattr(dim_table, primary_key) == getattr(record, primary_key)).first()
        )

        if not existing_record:
            # TODO: use bulk_insert_mappings
            new_record = dim_table(
                **{column: getattr(record, column) for column in columns},
                create_dt=func.current_timestamp(),
            )
            session.add(new_record)
        else:
            # TODO: use bulk_update_mappings
            if any(
                getattr(existing_record, column) != getattr(record, column)
                for column in columns
                if column != primary_key
            ):
                for column in columns:
                    if column == primary_key:
                        continue
                    setattr(existing_record, column, getattr(record, column))
                existing_record.update_dt = func.current_timestamp()


@provide_session
def load_tables_to_dim(session: Session, source_list: Sequence[Source] = DEFAULT_SOURCE_LIST) -> None:
    """Загружает данные в dim таблицы."""
    dim_source_list = list(filter(lambda source: isinstance(source, DimSource), source_list))
    for dim_source in dim_source_list:
        _load_to_dim(session=session, dim_source=dim_source)
