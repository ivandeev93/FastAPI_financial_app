from app.database import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from app.enum import CurrencyEnum


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)



class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    currency: Mapped[CurrencyEnum]