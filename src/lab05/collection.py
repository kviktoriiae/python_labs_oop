"""
ЛР-5: Расширенная коллекция с поддержкой функционального стиля.
"""
from lab_base import BankAccount

class Lab5Collection:
    def __init__(self):
        self._items = []

    def add(self, item: BankAccount):
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только BankAccount")
        if any(acc.account_number == item.account_number for acc in self._items):
            raise ValueError("Счёт с таким номером уже существует")
        self._items.append(item)

    def remove(self, itemCount: BankAccount):
        self._items.remove(itemCount)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def sort_by(self, key_func):
        """Сортировка коллекции на месте. Возвращает self для цепочки."""
        self._items.sort(key=key_func)
        return self

    def filter_by(self, predicate):
        """Фильтрация. Возвращает НОВЫЙ экземпляр Lab5Collection."""
        new_col = Lab5Collection()
        new_col._items = list(filter(predicate, self._items))
        return new_col

    def apply(self, func):
        """Применение функции ко всем элементам (мутация). Возвращает self."""
        self._items = list(map(func, self._items))
        return self

    def map_to_list(self, func):
        """Трансформация элементов в обычный список результатов."""
        return list(map(func, self._items))

    def __str__(self):
        if not self._items:
            return "Коллекция пуста."
        items_str = "\n  ".join([str(item) for item in self._items])
        return f"Lab5Collection ({len(self._items)} элементов):\n  {items_str}"
