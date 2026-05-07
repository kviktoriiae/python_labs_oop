from interfaces import Printable, Comparable, Exportable


# ── Валидаторы (из ЛР-1) ──────────────────────────────────────────────────────

def validate_owner(value: str):
    if not isinstance(value, str):
        raise TypeError("Владелец должен быть строкой")
    if not value.strip():
        raise ValueError("Имя владельца не может быть пустым")


def validate_ID(value: str):
    if not isinstance(value, str):
        raise TypeError("Номер счёта должен быть строкой")
    if len(value) != 10:
        raise ValueError("Номер счёта должен состоять ровно из 10 цифр")


def validate_currency(value: str):
    allowed = {"USD", "EUR", "RUB"}
    if not isinstance(value, str):
        raise TypeError("Валюта должна быть строкой")
    if value.upper() not in allowed:
        raise ValueError(f"Валюта должна быть одной из возможных({allowed})")


def validate_positive(value: float, field_name: str):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} должно быть числом")
    if value < 0:
        raise ValueError(f"{field_name} не может быть отрицательным")


# ── BankAccount ───────────────────────────────────────────────────────────────

class BankAccount(Printable, Comparable, Exportable):
    """
    Банковский счёт.
    Реализует интерфейсы: Printable, Comparable, Exportable.
    """

    name = "KVEbank"

    def __init__(self, account_ID, owner, balance, currency, overdraft_limit=0):
        validate_ID(account_ID)
        validate_owner(owner)
        validate_currency(currency)
        validate_positive(overdraft_limit, "лимит овердрафта")

        if balance < -overdraft_limit:
            raise ValueError("Баланс превышает допустимый овердрафт")

        self._account_number = account_ID
        self._owner = owner
        self._balance = float(balance)
        self._currency = currency.upper()
        self._overdraft_limit = float(overdraft_limit)
        self._is_active = True

    # ── Свойства ──────────────────────────────────────────────────────────────

    @property
    def account_number(self):
        return self._account_number

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        validate_owner(value)
        self._owner = value

    @property
    def balance(self):
        return self._balance

    @property
    def currency(self):
        return self._currency

    @property
    def is_active(self):
        return self._is_active

    # ── Бизнес-методы ─────────────────────────────────────────────────────────

    def deposit(self, amount):
        self._ensure_active()
        validate_positive(amount, "Сумма пополнения")
        self._balance += amount

    def withdraw(self, amount):
        self._ensure_active()
        validate_positive(amount, "Сумма снятия")
        if self._balance - amount < -self._overdraft_limit:
            raise ValueError("Лимит овердрафта превышен")
        self._balance -= amount

    def close(self):
        self._is_active = False

    def _ensure_active(self):
        if not self._is_active:
            raise RuntimeError("Операция невозможна: счёт закрыт")

    # ── Printable ─────────────────────────────────────────────────────────────

    def to_string(self) -> str:
        """Полное представление счёта."""
        status = "активный" if self._is_active else "закрытый"
        return (
            f"{self.name} | "
            f"Счёт №: {self._account_number} | "
            f"Владелец: {self._owner} | "
            f"Баланс: {self._balance:.2f} {self._currency} | "
            f"Статус: {status}"
        )

    def to_short_string(self) -> str:
        """Краткое представление: номер и баланс."""
        return f"[{self._account_number}] {self._owner}: {self._balance:.2f} {self._currency}"

    # ── Comparable ────────────────────────────────────────────────────────────

    def compare_to(self, other: "BankAccount") -> int:
        """Сравнение по балансу."""
        if not isinstance(other, BankAccount):
            raise TypeError("Можно сравнивать только с BankAccount")
        if self._balance < other._balance:
            return -1
        if self._balance > other._balance:
            return 1
        return 0

    # ── Exportable ────────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Экспорт данных счёта в словарь."""
        return {
            "account_number": self._account_number,
            "owner": self._owner,
            "balance": self._balance,
            "currency": self._currency,
            "overdraft_limit": self._overdraft_limit,
            "is_active": self._is_active,
        }

    # ── Магические методы ─────────────────────────────────────────────────────

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return (
            f"BankAccount('{self._account_number}', "
            f"'{self._owner}', {self._balance}, "
            f"'{self._currency}', {self._overdraft_limit})"
        )

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number


# ── SavingsAccount (расширенный тип — тоже реализует интерфейсы) ──────────────

class SavingsAccount(BankAccount):
    """
    Накопительный счёт с процентной ставкой.
    Наследует BankAccount и переопределяет методы интерфейсов.
    """

    def __init__(self, account_ID, owner, balance, currency, interest_rate: float):
        super().__init__(account_ID, owner, balance, currency, overdraft_limit=0)
        if not isinstance(interest_rate, (int, float)) or interest_rate < 0:
            raise ValueError("Процентная ставка должна быть неотрицательным числом")
        self._interest_rate = float(interest_rate)

    @property
    def interest_rate(self):
        return self._interest_rate

    def accrue_interest(self):
        """Начислить проценты на текущий баланс."""
        self._ensure_active()
        self._balance += self._balance * self._interest_rate / 100

    # ── Printable (другая реализация) ─────────────────────────────────────────

    def to_string(self) -> str:
        """Полное представление накопительного счёта (включает ставку)."""
        status = "активный" if self._is_active else "закрытый"
        return (
            f"{self.name} [НАКОПИТЕЛЬНЫЙ] | "
            f"Счёт №: {self._account_number} | "
            f"Владелец: {self._owner} | "
            f"Баланс: {self._balance:.2f} {self._currency} | "
            f"Ставка: {self._interest_rate:.1f}% | "
            f"Статус: {status}"
        )

    def to_short_string(self) -> str:
        """Краткое представление с пометкой о ставке."""
        return (
            f"[{self._account_number}] {self._owner}: "
            f"{self._balance:.2f} {self._currency} @ {self._interest_rate:.1f}%"
        )

    # ── Comparable (другая реализация — сравнение с учётом ставки) ────────────

    def compare_to(self, other) -> int:
        """
        Сравнение по «доходному потенциалу»: balance * (1 + rate/100).
        Для обычных BankAccount rate = 0.
        """
        if not isinstance(other, BankAccount):
            raise TypeError("Можно сравнивать только с BankAccount")

        my_value = self._balance * (1 + self._interest_rate / 100)
        other_rate = getattr(other, "_interest_rate", 0.0)
        other_value = other.balance * (1 + other_rate / 100)

        if my_value < other_value:
            return -1
        if my_value > other_value:
            return 1
        return 0

    # ── Exportable (другая реализация) ────────────────────────────────────────

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["interest_rate"] = self._interest_rate
        base["type"] = "savings"
        return base


# ── BankAccountCollection ─────────────────────────────────────────────────────

class BankAccountCollection:
    """
    Коллекция банковских счётов (из ЛР-2), расширенная методами для работы
    с объектами через интерфейсы Printable, Comparable и Exportable.
    """

    def __init__(self):
        self._items: list[BankAccount] = []

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def add(self, item: BankAccount):
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только BankAccount")
        if any(acc.account_number == item.account_number for acc in self._items):
            raise ValueError("Счёт с таким номером уже существует")
        self._items.append(item)

    def remove(self, item: BankAccount):
        self._items.remove(item)

    def remove_at(self, index: int):
        if index < 0 or index >= len(self._items):
            raise IndexError("Неверный индекс")
        del self._items[index]

    def get_all(self):
        return self._items.copy()

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    # ── Поиск ─────────────────────────────────────────────────────────────────

    def find_by_id(self, account_number):
        for acc in self._items:
            if acc.account_number == account_number:
                return acc
        return None

    def find_by_owner(self, owner: str):
        return [acc for acc in self._items if acc.owner == owner]

    # ── Сортировка ────────────────────────────────────────────────────────────

    def sort_by_balance(self):
        self._items.sort(key=lambda acc: acc.balance)

    def sort_by_owner(self):
        self._items.sort(key=lambda acc: acc.owner)

    def sort_by_comparable(self):
        """Сортировка через интерфейс Comparable (полиморфно, без isinstance)."""
        for i in range(len(self._items)):
            for j in range(i + 1, len(self._items)):
                if self._items[i].compare_to(self._items[j]) > 0:
                    self._items[i], self._items[j] = self._items[j], self._items[i]

    # ── Фильтрация по обычным признакам ──────────────────────────────────────

    def get_active(self) -> "BankAccountCollection":
        col = BankAccountCollection()
        for acc in self._items:
            if acc.is_active:
                col.add(acc)
        return col

    def get_inactive(self) -> "BankAccountCollection":
        col = BankAccountCollection()
        for acc in self._items:
            if not acc.is_active:
                col.add(acc)
        return col

    def get_rich(self, min_balance: float) -> "BankAccountCollection":
        col = BankAccountCollection()
        for acc in self._items:
            if acc.balance >= min_balance:
                col.add(acc)
        return col

    # ── Фильтрация по интерфейсам (задание на 5) ──────────────────────────────

    def get_printable(self) -> list[Printable]:
        """Вернуть все объекты, реализующие Printable."""
        return [acc for acc in self._items if isinstance(acc, Printable)]

    def get_comparable(self) -> list[Comparable]:
        """Вернуть все объекты, реализующие Comparable."""
        return [acc for acc in self._items if isinstance(acc, Comparable)]

    def get_exportable(self) -> list[Exportable]:
        """Вернуть все объекты, реализующие Exportable."""
        return [acc for acc in self._items if isinstance(acc, Exportable)]

    # ── Работа через интерфейсы ───────────────────────────────────────────────

    def print_all(self) -> None:
        """Вывести все объекты через интерфейс Printable (полиморфно)."""
        for item in self.get_printable():
            print(item.to_string())

    def export_all(self) -> list[dict]:
        """Экспортировать все объекты через интерфейс Exportable."""
        return [item.to_dict() for item in self.get_exportable()]