from app.database import SessionLocal
from app.models import Wallet
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models import User


def is_wallet_exist(db: Session, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None


def add_income(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.balance += amount
    return wallet


def get_wallet_balance_by_name(db: Session, wallet_name: str) -> Wallet:
     return db.query(Wallet).filter(Wallet.name == wallet_name).first()


def add_expense(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.balance -= amount
    return wallet


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    return db.query(Wallet).filter(User.id == user_id).all()


def create_wallet(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount)
    db.add(wallet)
    db.flush()
    return wallet
