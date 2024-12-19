import datetime
from dataclasses import field
from typing import Literal

from modules.models import Base
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Source:
    """Описание источников для загрузки в базу."""

    path: str
    source_type: Literal["file", "table"]
    target_table: type[Base]
    validator: BaseModel | None = field(default=None)

    def __post_init__(self) -> None:
        """Выставление даты в путь файла."""
        self.path = self.path.format(today=datetime.date.today().strftime("%d%m%Y"))
