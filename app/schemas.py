from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

from app.enum import CurrencyEnum


# Модель для описания операции с деньгами
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    # Валидатор для проверки, что сумма положительная
    @field_validator('amount')
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        # Проверяем что значение больше нуля
        if v <= 0:
            raise ValueError("Amount must be positive")
        # Возвращаем значение если все ок
        return v

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем что строка не пустая
        if not v:
            raise ValueError("Wallet name cannot be empty")
        # Возвращаем очищенное значение
        return v


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0

    currency: CurrencyEnum.RUB

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем что строка не пустая
        if not v:
            raise ValueError("Wallet name cannot be empty")
        # Возвращаем очищенное значение
        return v

    @field_validator('initial_balance')
    def balance_not_negative(cls, v: Decimal) -> Decimal:
        # Проверяем что значение больше нуля
        if v < 0:
            raise ValueError("Initial balance cannot be negative")
        # Возвращаем значение если все ок
        return v


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    
    
class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    
    id: int


class WalletResponse(BaseModel):
    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum