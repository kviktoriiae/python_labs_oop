from model import BankAccount
from collection import BankAccountCollection


def print_collection(collection, title):
    print(f"\n--- {title} ---")
    for item in collection:
        print(item)


def main():
    collection = BankAccountCollection()

    # создаём аккаунты
    acc1 = BankAccount("1234567890","Виктория",1000,"USD",500)
    acc2 = BankAccount("2345678901", "Bob", 500, "EUR", 1000)
    acc3 = BankAccount("3456789012", "Alice", 100, "USD", 600)

    # Сценарий 1 — базовая работа
    print("\n=== Сценарий 1: Добавление и вывод ===")
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)

    print("\n=== Все счета через for ===")
    for acc in collection:
        print(acc) 
    # Сценарий 2 — поиск, индекс, удаление
    print("\n=== Сценарий 2: Поиск и индексация ===")
    print("Поиск по номеру:", collection.find_by_id("1234567890"))
    print("Поиск по владельцу:", collection.find_by_owner("Alice"))
    print("Первый элемент:", collection[0])  # __getitem__

    collection.remove_at(1)
    print_collection(collection, "После удаления по индексу")

    # Сценарий 3 — сортировка и фильтрация
    print("\n=== Сценарий 3: Сортировка и фильтрация ===")

    collection.sort_by_balance()
    print_collection(collection, "Сортировка по балансу")

    collection.sort_by_owner()
    print_collection(collection, "Сортировка по владельцу")

    print_collection(collection.get_rich(1500), "Баланс >= 1500")

    acc3.close()  # делаем один закрытым
    print_collection(collection.get_active(), "Активные счета")
    print_collection(collection.get_inactive(), "Неактивные счета")

    # проверка дубликата
    print("\n=== Проверка ошибок ===")
    try:
        collection.add(BankAccount("3456789012", "Alice", 2000, "USD", 600))
    except ValueError as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()