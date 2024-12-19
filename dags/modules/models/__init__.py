from sqlalchemy import Engine

from modules.models.account import AccountModel, DimAccount, DimAccountHist, StagingAccount
from modules.models.base import Base, DeclarativeBase
from modules.models.blacklist import BlacklistModel, FactPassportBlacklist, StagingPassportBlacklist
from modules.models.card import CardModel, DimCard, DimCardHist, StagingCard
from modules.models.client import ClientModel, DimClient, DimClientHist, StagingClient
from modules.models.report import FraudReport
from modules.models.terminal import DimTerminal, DimTerminalHist, StagingTerminal, TerminalModel
from modules.models.transaction import FactTransaction, StagingTransaction, TransactionModel


def create_tables(engine: Engine) -> None:
    """Создает все ещё несозданные таблицы."""
    DeclarativeBase.metadata.create_all(bind=engine)


__all__ = [
    "AccountModel",
    "Base",
    "BlacklistModel",
    "CardModel",
    "ClientModel",
    "DeclarativeBase",
    "DimAccount",
    "DimAccountHist",
    "DimCard",
    "DimCardHist",
    "DimClient",
    "DimClientHist",
    "DimTerminal",
    "DimTerminalHist",
    "FactPassportBlacklist",
    "FactTransaction",
    "FraudReport",
    "StagingAccount",
    "StagingCard",
    "StagingClient",
    "StagingPassportBlacklist",
    "StagingTerminal",
    "StagingTransaction",
    "TerminalModel",
    "TransactionModel",
    "create_tables",
]
