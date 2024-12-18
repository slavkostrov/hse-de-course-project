import logging
import os

from sqlalchemy.orm import declarative_base, declared_attr

TABLE_PREFIX_ENV_VAR = "TABLE_PREFIX"
TABLE_PREFIX = os.get(TABLE_PREFIX_ENV_VAR)
if not TABLE_PREFIX:
    raise RuntimeError("env variable 'TABLE_PREFIX_ENV_VAR' not found")
else:
    logging.debug("found env variable for table_prefix: %s", TABLE_PREFIX)

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """Base class for ORM models definition."""

    @declared_attr
    def __tablename__(cls):  # noqa
        return f"{TABLE_PREFIX}_{cls.__name__.lower()}"
