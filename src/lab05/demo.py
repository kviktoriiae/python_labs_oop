import sys
import os

from lab_base import BankAccount, SavingsAccount, CreditAccount
from collection import Lab5Collection
import strategies as st

def main():
    # Инициализация коллекции 
    print("       1. Инициализация коллекции       ")
    bank = Lab5Collection()
    
    # ID должен быть 10 цифр по валидации
    bank.add(BankAccount("1234567890", "Виктория", 500000.0, "RUB"))
    bank.add(SavingsAccount("2345678901", "Артемий", 1500.0, "USD", 0.05))
    bank.add(CreditAccount("3456789012", "Бедолага", -2000.0, "EUR", 10000, 0.15))
    bank.add(BankAccount("5678901234", "Ульяна", 1500.0, "USD"))
    bank.add(SavingsAccount("0987654321", "Светлана", 2500.0, "USD", 0.03))
    print(bank)

    # Сортировка 
    print("\n       2. Сортировка по Владельцу (Стратегия)       ")
    bank.sort_by(st.sort_by_owner)
    print(bank)

    print("\n       3. Сортировка по Балансу (Lambda)       ")
    bank.sort_by(lambda acc: acc.balance)
    print(bank)

    # Фильтрация 
    print("\n       4. Фильтрация: Счета в USD       ")
    usd_accounts = bank.filter_by(st.is_usd_account)
    print(usd_accounts)

    # Map и Трансформации 
    print("\n       5. Map: Список имен владельцев (Lambda)       ")
    names = bank.map_to_list(lambda acc: acc.owner)
    print(f"Имена: {names}")

    print("\n       6. Использование Фабрики Фильтров (Баланс >= 1000)       ")
    min_bal_filter = st.make_min_balance_filter(1000)
    rich_accounts = bank.filter_by(min_bal_filter)
    print(rich_accounts)

    #Паттерн Стратегия и Цепочки ]
    print("\n       7. Сценарий: Цепочка операций (Filter -> Sort -> Apply)       ")
    # Фильтруем рублевые счета, сортируем по балансу и начисляем бонус 100 RUB
    bonus_100 = st.BonusStrategy(100.0)
    
    result = (bank
              .filter_by(lambda acc: acc.currency == "RUB")
              .sort_by(st.sort_by_balance)
              .apply(bonus_100))
    
    print("Результат цепочки (RUB счета + бонус 100):")
    print(result)

    print("\n       8. Замена стратегии (Callable-объект TaxStrategy)       ")
    tax_10_percent = st.TaxStrategy(0.10)
    
    print("До налога:")
    print(bank[0])
    # Применяем налог к первому счету через фильтр и apply
    bank.filter_by(lambda acc: acc.owner == bank[0].owner).apply(tax_10_percent)
    print("После налога (10%):")
    print(bank[0])

if __name__ == "__main__":
    main()
