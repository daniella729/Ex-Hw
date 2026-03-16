from enum import Enum
from sqlalchemy import (
    Enum as SqlEnum,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from solution.database import Base

SYSTEM_CURRENCY = "ILS"
MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    category_type: Mapped[CategoryType] = mapped_column(
        SqlEnum(CategoryType), nullable=False
    )
    is_archived: Mapped[bool] = mapped_column(default=False, nullable=False)
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
