from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository
from fastapi import HTTPException


def get_wallet(wallet_name: str | None = None):
    # Если имя кошелька не указано - считаем общий баланс
    if wallet_name is None:
        # Суммируем все значения из словаря BALANCE
        wallets = wallets_repository.get_all_wallets()
        return {"total_balance": sum(wallets.values())}

    # Проверяем существует ли запрашиваемый кошелек
    if not wallets_repository.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    # Возвращаем баланс конкретного кошелька
    balance = wallets_repository.get_wallet_balance_by_name(wallet_name)
    return {"wallet": wallet_name, "balance": balance}

def create_wallet(wallet: CreateWalletRequest):
    # Проверяем не существует ли уже такой кошелек
    if wallets_repository.is_wallet_exist(wallet.name):
        raise HTTPException(
            # Если кошелек уже есть - возвращаем ошибку 400
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )
    # Создаем новый кошелек с начальным балансом
    new_balance = wallets_repository.create_wallet(wallet.name, wallet.initial_balance)
    # Возвращаем информацию о созданном кошельке
    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "balance": new_balance
    }