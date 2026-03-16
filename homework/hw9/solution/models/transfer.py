from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship

from solution.database import Base
import datetime

MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100


class Transfer(Base):
    __tablename__ = "transfers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transfer_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False
    )
    to_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    from_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="outgoing_transfers",
    )
    to_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="incoming_transfers",
    )
