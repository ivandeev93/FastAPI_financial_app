from app.database import Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal]