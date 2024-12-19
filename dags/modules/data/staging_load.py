from modules.data.source import Source
from modules.models import (
    AccountModel,
    Blacklist,
    BlacklistModel,
    CardModel,
    ClientModel,
    StagingAccount,
    StagingCard,
    StagingClient,
    StagingTerminal,
    StagingTransaction,
    TerminalModel,
    TransactionModel,
)

DEFAULT_DATA_PATH = "."
DEFAULT_SOURCE_LIST = (
    Source(
        path=f"{DEFAULT_DATA_PATH}/transactions_DDMMYYYY.xlsx",
        source_type="file",
        target_table=StagingTransaction,
        validator=TransactionModel,
    ),
    Source(
        path=f"{DEFAULT_DATA_PATH}/terminals_DDMMYYYY.xlsx",
        source_type="file",
        target_table=StagingTerminal,
        validator=TerminalModel,
    ),
    Source(
        path=f"{DEFAULT_DATA_PATH}/passport_blacklist_DDMMYYYY.xlsx",
        source_type="file",
        target_table=Blacklist,
        validator=BlacklistModel,
    ),
    Source(
        path="info.clients",
        source_type="table",
        target_table=StagingClient,
        validator=ClientModel,
    ),
    Source(
        path="info.cards",
        source_type="table",
        target_table=StagingCard,
        validator=CardModel,
    ),
    Source(
        path="info.accounts",
        source_type="table",
        target_table=StagingAccount,
        validator=AccountModel,
    ),
)

# def load_data_into_staging()
