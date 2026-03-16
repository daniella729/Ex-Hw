from dataclasses import dataclass

import datetime
from enum import Enum

from sqlalchemy import (
    Integer,
    Numeric,
    String,
)
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship

from solution.database import Base

SYSTEM_CURRENCY = "ILS"
MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), default=SYSTEM_CURRENCY, nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account"
    )
    outgoing_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer",
        foreign_keys="Transfer.from_account_id",
        back_populates="from_account",
    )
    incoming_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account"
    )
