from base import BankAccount

# Накопительный счёт 
class SavingsAccount(BankAccount):
    def __init__(self, account_ID, owner, balance, currency, interest_rate):
        super().__init__(account_ID, owner, balance, currency)
        self.interest_rate = interest_rate  # новый атрибут
        self.account_type = "savings"       # новый атрибут

    def apply_interest(self): # Начисление процентов
        self._balance += self._balance * self.interest_rate

    def calculate(self): # Полиморфный метод
        return self._balance * self.interest_rate

    def __str__(self):
        return super().__str__() + f" | Тип: накопительный | Ставка: {self.interest_rate}"


# Кредитный счёт
class CreditAccount(BankAccount):
    def __init__(self, account_ID, owner, balance, currency, credit_limit, interest_rate):
        super().__init__(account_ID, owner, balance, currency, overdraft_limit=credit_limit)
        self.credit_limit = credit_limit   # новый атрибут
        self.interest_rate = interest_rate # новый атрибут

    def charge_interest(self):
        #Начисление процентов на долг
        if self._balance < 0:
            self._balance += self._balance * self.interest_rate

    def calculate(self): # Полиморфный метод
        if self._balance < 0:
            return self._balance * self.interest_rate
        return 0

    def __str__(self):
        return super().__str__() + f" | Тип: кредитный | Лимит: {self.credit_limit}"

    def get_credit(self):
        return [acc for acc in self._items if isinstance(acc, CreditAccount)]