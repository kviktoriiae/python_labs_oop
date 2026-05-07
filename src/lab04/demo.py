from base import BankAccount, SavingsAccount, BankAccountCollection
from interfaces import Printable, Comparable, Exportable
import json

def print_all(items: list[Printable]) -> None:
    for item in items:
        print(item.to_string())


def print_short(items: list[Printable]) -> None:
    """Краткий вывод через интерфейс Printable."""
    for item in items:
        print("  •", item.to_short_string())


def sort_by_interface(items: list[Comparable]) -> list[Comparable]:
    """Сортировка через интерфейс Comparable (без условий)."""
    sorted_items = items.copy()
    for i in range(len(sorted_items)):
        for j in range(i + 1, len(sorted_items)):
            if sorted_items[i].compare_to(sorted_items[j]) > 0:
                sorted_items[i], sorted_items[j] = sorted_items[j], sorted_items[i]
    return sorted_items


def export_all(items: list[Exportable]) -> list[dict]:
    """Универсальный экспорт через интерфейс Exportable."""
    return [item.to_dict() for item in items]


# ─────────────────────────────────────────────────────────────────────────────
# Подготовка данных
# ─────────────────────────────────────────────────────────────────────────────

def sep(title: str) -> None:
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print('═' * 60)


accounts = [
    BankAccount("1234567890", "Виктория",   5000,  "USD"),
    BankAccount("0987654321", "Артемий", 1500.50, "RUB"),
    SavingsAccount("2222222222", "Светлана",   30000, "RUB", interest_rate=7.5),
    SavingsAccount("3333333333", "Ульяна", 9000, "USD", interest_rate=3.0),
]

# Закроем один счёт для наглядности
accounts[2].close()

collection = BankAccountCollection()
for acc in accounts:
    collection.add(acc)

# Сценарий 1 — Полиморфный вывод через интерфейс Printable
sep("Printable: полиморфный вывод")
print("\nПолный вывод через print_all(items: list[Printable])")
print_all(accounts)

print("\nКраткий вывод через print_short(items: list[Printable])")
print_short(accounts)

print("\nBankAccount и SavingsAccount дают разный вывод — полиморфизм:")
ba = accounts[0]   # BankAccount
sa = accounts[3]   # SavingsAccount
print(f"  BankAccount    → {ba.to_short_string()}")
print(f"  SavingsAccount → {sa.to_short_string()}")


# ─────────────────────────────────────────────────────────────────────────────
# Сценарий 2 — Сравнение и сортировка через интерфейс Comparable
# ─────────────────────────────────────────────────────────────────────────────

sep("Comparable: сравнение и сортировка")

print("\nПрямое сравнение двух счётов через compare_to()")
a1, a2 = accounts[0], accounts[1]
result = a1.compare_to(a2)
sign = {-1: "<", 0: "=", 1: ">"}[result]
print(f"  {a1.to_short_string()}")
print(f"    compare_to →  {sign}")
print(f"  {a2.to_short_string()}")


print("\nСортировка через sort_by_interface() — без единого isinstance внутри функции")
sorted_accounts = sort_by_interface(accounts)
print_short(sorted_accounts)

print("\nСортировка коллекции через sort_by_comparable()")
collection.sort_by_comparable()
collection.print_all()


# ─────────────────────────────────────────────────────────────────────────────
# Сценарий 3 — Экспорт через интерфейс Exportable
# ─────────────────────────────────────────────────────────────────────────────

sep(" Exportable: экспорт данных")

print("\nЭкспорт всех счётов через export_all(items: list[Exportable]")
exported = export_all(accounts)
print(json.dumps(exported, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# Сценарий 4 — Фильтрация коллекции по интерфейсам + isinstance
# ─────────────────────────────────────────────────────────────────────────────

sep("Фильтрация коллекции по интерфейсам")

printable_items  = collection.get_printable()
comparable_items = collection.get_comparable()
exportable_items = collection.get_exportable()

print(f"\n  Всего счётов в коллекции : {len(collection)}")
print(f"  Реализуют Printable      : {len(printable_items)}")
print(f"  Реализуют Comparable     : {len(comparable_items)}")
print(f"  Реализуют Exportable     : {len(exportable_items)}")

print("\nПроверка isinstance для каждого счёта")
for acc in collection:
    flags = []
    if isinstance(acc, Printable):
        flags.append("Printable")
    if isinstance(acc, Comparable):
        flags.append("Comparable")
    if isinstance(acc, Exportable):
        flags.append("Exportable")
    cls_name = type(acc).__name__
    print(f"  {acc.to_short_string():<45} [{cls_name}] → {', '.join(flags)}")

print("\nРабота через отфильтрованный список Printable из коллекции")
print_short(printable_items)

print()