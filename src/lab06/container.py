from typing import TypeVar, Generic, Callable, Optional, Protocol, runtime_checkable

# Обобщенные типы
T = TypeVar('T')
R = TypeVar('R')

#  Протоколы (Structural Subtyping) 

@runtime_checkable
class Displayable(Protocol):
    def display(self) -> str:
        ...

@runtime_checkable
class Scorable(Protocol):
    def score(self) -> float:
        ...

# Ограниченные типы для использования в типизированных коллекциях
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)

#  Обобщенная коллекция (Generics) 

class TypedCollection(Generic[T]):
    """
    Типизированная коллекция, реализующая Generic[T].
    Поддерживает базовые операции и функциональный стиль.
    """
    
    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        """Добавление элемента. Тип T проверяется статическими анализаторами."""
        self._items.append(item)

    def remove(self, item: T) -> None:
        """Удаление элемента из коллекции."""
        self._items.remove(item)

    def get_all(self) -> list[T]:
        """Возвращает копию списка всех элементов."""
        return list(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    # Функциональные методы

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Поиск первого элемента, удовлетворяющего условию."""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Возвращает список элементов, удовлетворяющих условию."""
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        """Применяет трансформацию к каждому элементу и возвращает список результатов типа R."""
        return [transform(item) for item in self._items]

    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection is empty."
        items_repr = "\n  ".join([str(i) for i in self._items])
        return f"TypedCollection with {len(self._items)} items:\n  {items_repr}"
