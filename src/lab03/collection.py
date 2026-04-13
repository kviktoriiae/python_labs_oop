from base import BankAccount
from model import SavingsAccount, CreditAccount

class BankAccountCollection:
    def __init__(self):
        self._items = []

    # добавление
    def add(self, item: BankAccount):
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только BankAccount")

        if any(acc.account_number == item.account_number for acc in self._items):
            raise ValueError("Счёт с таким номером уже существует")

        self._items.append(item)

    # удаление
    def remove(self, item: BankAccount):
        self._items.remove(item)

    def remove_at(self, index: int):
        if index < 0 or index >= len(self._items):
            raise IndexError("Неверный индекс")
        del self._items[index]

    # получение
    def get_all(self):
        return self._items.copy()

    def __getitem__(self, index):
        return self._items[index]

    # поиск
    def find_by_id(self, account_number):
        for acc in self._items:
            if acc.account_number == account_number:
                return acc
        return None

    def find_by_owner(self, owner: str):
        return [acc for acc in self._items if acc.owner == owner]

    # итерация
    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    # сортировка
    def sort(self, key=None):
        self._items.sort(key=key)

    def sort_by_balance(self):
        self._items.sort(key=lambda acc: acc.balance)

    def sort_by_owner(self):
        self._items.sort(key=lambda acc: acc.owner)

    # фильтрация
    def get_active(self):
        new_collection = BankAccountCollection()
        for acc in self._items:
            if acc.is_active:
                new_collection.add(acc)
        return new_collection

    def get_inactive(self):
        new_collection = BankAccountCollection()
        for acc in self._items:
            if not acc.is_active:
                new_collection.add(acc)
        return new_collection

    def get_rich(self, min_balance: float):
        new_collection = BankAccountCollection()
        for acc in self._items:
            if acc.balance >= min_balance:
                new_collection.add(acc)
        return new_collection
    def get_savings(self):
        return [acc for acc in self._items if isinstance(acc, SavingsAccount)]

    def get_credit(self):
        return [acc for acc in self._items if isinstance(acc, CreditAccount)]