import functools
from typing import Any

import psycopg2
import sqlalchemy
from modules.settings import db_settings
from sqlalchemy.orm import scoped_session, sessionmaker

creator = functools.partial(
    psycopg2.connect,
    database=db_settings.database,
    host=db_settings.host.get_secret_value(),
    user=db_settings.user.get_secret_value(),
    password=db_settings.password.get_secret_value(),
    port=db_settings.port,
)

engine = sqlalchemy.create_engine(
    "postgresql+psycopg2://",
    creator=creator,
    echo=db_settings.verbose,
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def provide_session(func: callable) -> callable:
    """Provide session decorator."""

    @functools.wraps(func)
    def inner(*args, **kwargs) -> Any:
        session = kwargs.pop("session", Session())
        try:
            value = func(session=session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            Session.remove()
        return value

    return inner
