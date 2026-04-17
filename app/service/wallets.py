from app.database import SessionLocal
from app.enum import CurrencyEnum
from app.schemas import CreateWalletRequest, TotalBalance, WalletResponse
from app.repository import wallets as wallets_repository
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.service import exchange_service
from decimal import Decimal


async def get_total_balance(db: Session, current_user: User) -> TotalBalance:
    """
    Получает баланс кошелька или общий баланс всех кошельков пользователя

    Args:
        db:
        current_user:

    Returns:
        Словарь с информацией о балансе (либо конкретного кошелька, либо общий баланс)

    Raises:
        HTTPException: Если указанный кошелек не найден
    """
    # Если имя кошелька не указано - считаем общий баланс
    wallets = wallets_repository.get_all_wallets(db, current_user.id)
    total_balance = Decimal(0)

    for wallet in wallets:
        if wallet.currency == CurrencyEnum.RUB:
            total_balance += wallet.balance
        else:
            exchange_rate = await exchange_service.get_exchange_rate(wallet.currency, CurrencyEnum.RUB)
            total_balance += exchange_rate * wallet.balance

    return TotalBalance(total_balance=total_balance)



def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest) -> WalletResponse:
    # Проверяем не существует ли уже такой кошелек
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(
            # Если кошелек уже есть - возвращаем ошибку 400
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )
    # Создаем новый кошелек с начальным балансом
    wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    db.commit()
    # Возвращаем информацию о созданном кошельке
    return WalletResponse.model_validate(wallet)


def get_all_wallets(db: Session, current_user: User) -> list[WalletResponse]:
    wallets = wallets_repository.get_all_wallets(db, current_user.id)
    return [WalletResponse.model_validate(wallet) for wallet in wallets]