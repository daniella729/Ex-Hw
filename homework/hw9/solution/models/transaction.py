import datetime
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

MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions"
    )
    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
