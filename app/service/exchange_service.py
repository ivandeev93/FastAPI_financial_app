from decimal import Decimal
from typing import Dict, Tuple
import aiohttp
from app.enum import CurrencyEnum

# курсы валют
FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),  # Примерный курс USD->RUB
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),  # Примерный курс USD->EUR
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),  # Примерный курс EUR->RUB
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),  # Примерный курс RUB->USD
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),  # Примерный курс EUR->USD
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097)),  # Примерный курс RUB->EUR
}


async def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    """
    Получает курс обмена между двумя валютами

    Args:
        base: Базовая валюта (из которой конвертируем)
        target: Целевая валюта (в которую конвертируем)

    Returns:
        Курс обмена (сколько единиц целевой валюты за одну единицу базовой)
        Если курс не найден - возвращает 1 (без конвертации)
    """

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"


    timeout = aiohttp.ClientTimeout(total=5.0)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                base_map = data.get(base, {})
                rate = base_map.get(target)

        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found")

    except Exception:
        # Ищем курс в словаре резервных курсов
        # Если курс не найден - возвращаем 1 (без конвертации)
        return FALLBACK_RATES.get((base, target), Decimal(1))