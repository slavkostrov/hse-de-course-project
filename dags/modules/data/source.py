from typing import Literal

from modules.models import (
    AccountModel,
    Base,
    BlacklistModel,
    CardModel,
    ClientModel,
    DimAccount,
    DimAccountHist,
    DimCard,
    DimCardHist,
    DimClient,
    DimClientHist,
    DimTerminal,
    DimTerminalHist,
    FactPassportBlacklist,
    FactTransaction,
    StagingAccount,
    StagingCard,
    StagingClient,
    StagingPassportBlacklist,
    StagingTerminal,
    StagingTransaction,
    TerminalModel,
    TransactionModel,
)
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Source:
    """Описание источников для загрузки в базу."""

    path: str
    source_type: Literal["table", "txt", "excel"]
    target_table: type[Base]
    validator: type[BaseModel]

    def __post_init__(self) -> None:
        """Выставление даты в путь файла."""
        self.path = self.path.format(today="02032021")  # datetime.date.today().strftime("%d%m%Y"))


@dataclass
class DimSource(Source):
    """Описание Dim источника."""

    dim_table: type[Base]
    dim_hist_table: type[Base]


@dataclass
class FactSource(Source):
    """Описание Fact источника."""

    fact_table: type[Base]


# TODO: fix
DEFAULT_DATA_PATH = "../data"
DEFAULT_SOURCE_LIST = (
    DimSource(
        path="info.clients",
        source_type="table",
        target_table=StagingClient,
        validator=ClientModel,
        dim_table=DimClient,
        dim_hist_table=DimClientHist,
    ),
    DimSource(
        path=f"{DEFAULT_DATA_PATH}" + "/terminals_{today}.xlsx",
        source_type="excel",
        target_table=StagingTerminal,
        validator=TerminalModel,
        dim_table=DimTerminal,
        dim_hist_table=DimTerminalHist,
    ),
    DimSource(
        path="info.accounts",
        source_type="table",
        target_table=StagingAccount,
        validator=AccountModel,
        dim_table=DimAccount,
        dim_hist_table=DimAccountHist,
    ),
    DimSource(
        path="info.cards",
        source_type="table",
        target_table=StagingCard,
        validator=CardModel,
        dim_table=DimCard,
        dim_hist_table=DimCardHist,
    ),
    FactSource(
        path=f"{DEFAULT_DATA_PATH}" + "/transactions_{today}.txt",
        source_type="txt",
        target_table=StagingTransaction,
        validator=TransactionModel,
        fact_table=FactTransaction,
    ),
    FactSource(
        path=f"{DEFAULT_DATA_PATH}" + "/passport_blacklist_{today}.xlsx",
        source_type="excel",
        target_table=StagingPassportBlacklist,
        validator=BlacklistModel,
        fact_table=FactPassportBlacklist,
    ),
)
