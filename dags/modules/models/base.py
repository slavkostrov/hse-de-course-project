import logging
import os

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, declared_attr

TABLE_PREFIX_ENV_VAR = "TABLE_PREFIX"
TABLE_PREFIX = os.environ.get(TABLE_PREFIX_ENV_VAR)
if not TABLE_PREFIX:
    raise RuntimeError(f"env variable '{TABLE_PREFIX_ENV_VAR}' not found")
else:
    logging.debug("found env variable for table_prefix: %s", TABLE_PREFIX)


metadata = MetaData(schema="public")
DeclarativeBase = declarative_base(metadata=metadata)


class Base:
    """Base class for ORM models definition."""

    __custom_table_name__ = None

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return f"{TABLE_PREFIX}_{cls.__custom_table_name__ or cls.__name__.lower()}"
