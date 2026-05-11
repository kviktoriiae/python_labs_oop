from typing import Callable, Any

# Базовые стратегии сортировки и фильтрации 

def sort_by_owner(acc: Any) -> str:
    """Стратегия: сортировка по владельцу."""
    return acc.owner

def sort_by_balance(acc: Any) -> float:
    """Стратегия: сортировка по балансу."""
    return acc.balance

def sort_by_currency_and_balance(acc: Any) -> tuple:
    """Сложная стратегия: по валюте, затем по балансу."""
    return (acc.currency, acc.balance)

def filter_active(acc: Any) -> bool:
    """Фильтр: только активные счета."""
    return acc.is_active

def is_usd_account(acc: Any) -> bool:
    """Фильтр: счета в USD."""
    return acc.currency == "USD"

# Маппинг и Фабрики 

def to_full_dict(acc: Any) -> dict:
    """Преобразование объекта в расширенный словарь."""
    d = {
        "id": acc.account_number,
        "owner": acc.owner,
        "balance": acc.balance,
        "currency": acc.currency,
        "type": type(acc).__name__
    }
    return d

def make_min_balance_filter(min_val: float) -> Callable[[Any], bool]:
    """Фабрика фильтров по минимальному балансу."""
    def filter_fn(acc: Any) -> bool:
        return acc.balance >= min_val
    return filter_fn

def make_type_filter(acc_class: type) -> Callable[[Any], bool]:
    """Фабрика фильтров по типу класса (накопительные и кредитные счета)."""
    def filter_fn(acc: Any) -> bool:
        return isinstance(acc, acc_class)
    return filter_fn


class BonusStrategy:
    # Стратегия начисления бонуса. 
    
    def __init__(self, bonus_amount: float):
        self.bonus_amount = bonus_amount

    def __call__(self, acc: Any) -> Any:
        if acc.is_active:
            acc.deposit(self.bonus_amount)
        return acc

class TaxStrategy:
    """Стратегия списания налога с баланса."""
    def __init__(self, tax_rate: float):
        self.tax_rate = tax_rate

    def __call__(self, acc: Any) -> Any:
        tax = acc.balance * self.tax_rate
        if acc.balance >= tax:
            acc.withdraw(tax)
        return acc
