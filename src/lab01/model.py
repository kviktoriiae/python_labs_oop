from validate import  (validate_owner,validate_ID,validate_currency,validate_positive,)
class BankAccount:
    name = "KVEbank"
    def __init__(self, account_ID, owner, balance, currency, overdraft_limit=0):
        validate_ID(account_ID)
        validate_owner(owner)
        validate_currency(currency)
        validate_positive(overdraft_limit, "лимит овердрафта")

        if balance < -overdraft_limit:
            raise ValueError("баланс превышает допустимый овердрафт")
        
        # приватные атрибуты 
        self._account_number = account_ID
        self._owner = owner
        self._balance = float(balance)
        self._currency = currency.upper()
        self._overdraft_limit = float(overdraft_limit)
        self._is_active = True

    # безопасный доступ к приватным полям
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

    # бизнес-методы
    def deposit(self, amount):
        # пополнение счёта
        self._ensure_active()
        validate_positive(amount, "Сумма пополнения")
        self._balance += amount

    def withdraw(self, amount):
        # снятие средств с счёта
        self._ensure_active()
        validate_positive(amount, "Сумма снятия")
        if self._balance - amount < -self._overdraft_limit:
            raise ValueError("Лимит овердрафта превышен")
        self._balance -= amount

    def close(self):
        # закрытие счёта 
        self._is_active = False

    # внутренние методы (проверка состояния счета(открытый или закрытый))
    def _ensure_active(self):
        if not self._is_active:
            raise RuntimeError("Операция невозможна: счёт закрыт")

    # магические методы
    def __str__(self):
        status = "активный" if self._is_active else "закрытый"
        return (
            f"{self.name} | "
            f"Счет №: {self._account_number} | "
            f"Владелец: {self._owner} | "
            f"Баланс: {self._balance:.2f} {self._currency} | "
            f"Статус: {status}"
        )

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
    