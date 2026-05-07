from interfaces import Printable, Calculable
from base import BankAccount


class BankAccountCollection:
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только BankAccount")

        if any(acc.account_id == item.account_id for acc in self._items):
            raise ValueError("Счет уже существует")

        self._items.append(item)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def remove_at(self, index):
        del self._items[index]

    def get_printable(self):
        new = BankAccountCollection()
        for item in self._items:
            if isinstance(item, Printable):
                new.add(item)
        return new

    def get_calculable(self):
        new = BankAccountCollection()
        for item in self._items:
            if isinstance(item, Calculable):
                new.add(item)
        return new

    def sort_by_balance(self):
        self._items.sort(key=lambda x: x.balance)
