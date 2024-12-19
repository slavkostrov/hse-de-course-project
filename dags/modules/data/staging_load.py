import logging
from collections.abc import Sequence
from typing import Any

import pandas as pd
from modules.data.source import DEFAULT_SOURCE_LIST, Source
from modules.db.utils import provide_session
from pydantic import BaseModel, ValidationError
from sqlalchemy import Connection
from sqlalchemy.orm import Session

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def _load_data(source: Source, connection: Connection) -> pd.DataFrame:
    """Загружает данные из файла или из таблицы."""
    if source.source_type == "table":
        # TODO: check sql injections
        # TODO: iterate over batches?
        data = pd.read_sql(f"SELECT * FROM {source.path}", con=connection)  # noqa
    elif source.source_type == "excel":
        data = pd.read_excel(source.path)
    elif source.source_type == "txt":
        data = pd.read_csv(source.path, delimiter=";", decimal=",")
    else:
        raise RuntimeError(f"unknown source type - {source.source_type}")
    logging.info("loaded data from: %s", source.path)
    return data


def _validate_records(
    validator: BaseModel,
    records: list[dict[str, Any]],
    raise_on_error: bool = True,
) -> list[dict[str, Any]]:
    """Валидирует объекты с помощью Pydantic моделей."""
    validated_records = []
    for record in records:
        try:
            validated_records.append(validator(**record).model_dump())
        except ValidationError as e:
            if raise_on_error:
                raise
            logging.warning("got error while validating", exc_info=e)
    return validated_records


@provide_session
def load_data_into_staging(session: Session, source_list: Sequence[Source] = DEFAULT_SOURCE_LIST) -> None:
    """Загружает сырые данные в Staging."""
    for source in source_list:
        logging.info("start loading source: %s", source)
        data = _load_data(source, connection=session.connection())
        records = data.to_dict(orient="records")
        if source.validator is not None:
            logging.info("validate data with %s", source.validator)
            records = _validate_records(source.validator, records=records)
        logging.info("truncate target table before loading: %s", source.target_table)
        session.query(source.target_table).delete()
        session.bulk_insert_mappings(source.target_table, records)
        logging.info("loaded %s records into db", len(records))
