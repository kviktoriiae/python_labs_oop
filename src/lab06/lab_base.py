from typing import Optional, Any

# Валидация с аннотациями типов
def validate_owner(value: str) -> None:
    if not isinstance(value, str):
        raise TypeError("Владелец должен быть строкой")
    if not value.strip():
        raise ValueError("Имя владельца не может быть пустым")

def validate_ID(value: str) -> None:
    if not isinstance(value, str):
        raise TypeError("Номер счёта должен быть строкой")
    if len(value) != 10:
        raise ValueError("Номер счёта должен состоять ровно из 10 цифр")

def validate_currency(value: str) -> None:
    allowed = {"USD", "EUR", "RUB"}
    if not isinstance(value, str):
        raise TypeError("Валюта должна быть строкой")
    if value.upper() not in allowed:
        raise ValueError(f'Валюта должна быть одной из возможных({allowed})')

def validate_positive(value: float, field_name: str) -> None:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} должно быть числом")
    if value < 0:
        raise ValueError(f"{field_name} не может быть отрицательным")

class BankAccount:
    name: str = "KVEbank"
    
    def __init__(self, account_ID: str, owner: str, balance: float, currency: str, overdraft_limit: float = 0.0) -> None:
        validate_ID(account_ID)
        validate_owner(owner)
        validate_currency(currency)
        validate_positive(overdraft_limit, "лимит овердрафта")

        if balance < -overdraft_limit:
            raise ValueError("баланс превышает допустимый овердрафт")
        
        self._account_number: str = account_ID
        self._owner: str = owner
        self._balance: float = float(balance)
        self._currency: str = currency.upper()
        self._overdraft_limit: float = float(overdraft_limit)
        self._is_active: bool = True

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, value: str) -> None:
        validate_owner(value)
        self._owner = value

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def is_active(self) -> bool:
        return self._is_active

    def deposit(self, amount: float) -> None:
        self._ensure_active()
        validate_positive(amount, "Сумма пополнения")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        self._ensure_active()
        validate_positive(amount, "Сумма снятия")
        if self._balance - amount < -self._overdraft_limit:
            raise ValueError("Лимит овердрафта превышен")
        self._balance -= amount

    def close(self) -> None:
        self._is_active = False

    def _ensure_active(self) -> None:
        if not self._is_active:
            raise RuntimeError("Операция невозможна: счёт закрыт")

    # Методы для Протоколов 
    def display(self) -> str:
        """Реализация протокола Displayable."""
        return str(self)

    def score(self) -> float:
        """Реализация протокола Scorable (возвращает баланс как метрику счета)."""
        return self._balance

    def __str__(self) -> str:
        status = "активный" if self._is_active else "закрытый"
        return (
            f"{self.name} | "
            f"Счет №: {self._account_number} | "
            f"Владелец: {self._owner} | "
            f"Баланс: {self._balance:.2f} {self._currency} | "
            f"Статус: {status}"
        )

    def __repr__(self) -> str:
        return (
            f"BankAccount('{self._account_number}', "
            f"'{self._owner}', {self._balance}, "
            f"'{self._currency}', {self._overdraft_limit})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number

class SavingsAccount(BankAccount):
    def __init__(self, account_ID: str, owner: str, balance: float, currency: str, interest_rate: float) -> None:
        super().__init__(account_ID, owner, balance, currency)
        self.interest_rate: float = interest_rate
        self.account_type: str = "savings"

    def apply_interest(self) -> None:
        self._balance += self._balance * self.interest_rate

    def calculate(self) -> float:
        return self._balance * self.interest_rate

    def score(self) -> float:
        """Для накопительного счета скоринг учитывает потенциальную выгоду."""
        return self._balance + self.calculate()

    def __str__(self) -> str:
        return super().__str__() + f" | Тип: накопительный | Ставка: {self.interest_rate}"

class CreditAccount(BankAccount):
    def __init__(self, account_ID: str, owner: str, balance: float, currency: str, credit_limit: float, interest_rate: float) -> None:
        super().__init__(account_ID, owner, balance, currency, overdraft_limit=credit_limit)
        self.credit_limit: float = credit_limit
        self.interest_rate: float = interest_rate

    def charge_interest(self) -> None:
        if self._balance < 0:
            self._balance += self._balance * self.interest_rate

    def calculate(self) -> float:
        if self._balance < 0:
            return self._balance * self.interest_rate
        return 0.0

    def score(self) -> float:
        """Для кредитного счета высокий скоринг означает высокий кредитный лимит."""
        return self.credit_limit

    def __str__(self) -> str:
        return super().__str__() + f" | Тип: кредитный | Лимит: {self.credit_limit}"
