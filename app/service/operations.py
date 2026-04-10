from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository
from fastapi import HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session


def add_income(db: Session, operation: OperationRequest):
    # Проверяем существует ли кошелек
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Добавляем доход к балансу кошелька
    wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)
    db.commit()
    # Возвращаем информацию об операции
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }


def add_expense(db: Session, operation: OperationRequest):
    # Проверяем существует ли кошелек
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Проверяем достаточно ли средств в кошельке
    wallet = wallets_repository.get_wallet_balance_by_name(db, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Availabe: {wallet.balance}"
        )
    # Вычитаем расход из баланса кошелька
    wallet = wallets_repository.add_expense(db, operation.wallet_name, operation.amount)
    db.commit()
    # Возвращаем информацию об операции
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }
