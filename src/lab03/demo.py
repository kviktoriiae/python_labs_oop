from model import SavingsAccount, CreditAccount
from src.lib.collection import BankAccountCollection


def main():
    collection = BankAccountCollection()

    # создаем разные типы
    acc1 = SavingsAccount("1234567890", "Виктория", 20000, "USD", 0.05)
    acc2 = CreditAccount("2345678901", "Артемий", 5050, "EUR", 1000, 0.1)
    acc3 = SavingsAccount("3456789012", "Ульяна", 7777, "RUB", 0.03)

    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)

    # --- СЦЕНАРИЙ 1 ---
    print("\n=== Все счета ===")
    for acc in collection:
        print(acc)

    # --- СЦЕНАРИЙ 2 (ПОЛИМОРФИЗМ) ---
    print("\n=== Полиморфный метод ===")
    for acc in collection:
        print(acc.calculate())

    # --- СЦЕНАРИЙ 3 (ТИПЫ) ---
    print("\n=== Проверка типов ===")
    for acc in collection:
        if isinstance(acc, SavingsAccount):
            print("Накопительный:", acc)
        elif isinstance(acc, CreditAccount):
            print("Кредитный:    ", acc)

    # --- СЦЕНАРИЙ 4 (ФИЛЬТРАЦИЯ) ---
    print("\n=== Только накопительные ===")
    for acc in collection.get_savings():
        print(acc)

    print("\n=== Только кредитные ===")
    for acc in collection.get_credit():
        print(acc)


if __name__ == "__main__":
    main()