import sys
import os

from lab_base import BankAccount, SavingsAccount, CreditAccount
from container import TypedCollection, Displayable, Scorable, D, S

def main():
    # Сценарий 1: Обобщенная коллекция) 
    print("       1. Коллекция BankAccount        ")
    # Создаем коллекцию, работающую только с BankAccount (и его наследниками)
    accounts: TypedCollection[BankAccount] = TypedCollection()
    
    accounts.add(BankAccount("1234567890", "Виктория", 500000.0, "RUB"))
    accounts.add(SavingsAccount("2345678901", "Артемий", 1500.0, "USD", 0.05))
    accounts.add(CreditAccount("3456789012", "Бедолага", -2000.0, "EUR", 5000.0, 0.15))
    
    print(accounts)
    
    # --- Сценарий 2: Функциональные методы и TypeVar R 
    print("\n       2. Функциональные методы        ")
    
    # 2.1 Find (Optional[T])
    found = accounts.find(lambda acc: acc.owner == "Виктория")
    print(f"Найден владелец 'Виктория': {found}")
    
    not_found = accounts.find(lambda acc: acc.owner == "Кто-то несуществующий")
    print(f"Поиск несуществующего : {not_found}")
    
    # 2.2 Filter (list[T])
    usd_accs = accounts.filter(lambda acc: acc.currency == "USD")
    print(f"Счета в USD (список из {len(usd_accs)} элементов): {usd_accs}")
    
    # 2.3 Map (list[R]) - демонстрация смены типа
    # Была TypedCollection[BankAccount], получаем list[str] (только имена)
    names: list[str] = accounts.map(lambda acc: acc.owner)
    print(f"Результат map (только имена): {names}")
    
    # Получаем list[float] (только балансы)
    balances: list[float] = accounts.map(lambda acc: acc.balance)
    print(f"Результат map (балансы как float): {balances}")

    # --- Сценарий 3: Задание на 5 (Protocols) ---
    print("\n       3. Протоколы и структурная типизация        ")
    
    # 3.1 Protocol Displayable
    display_col: TypedCollection[Displayable] = TypedCollection()
    # Счета BankAccount реализуют метод display()
    display_col.add(BankAccount("7890123456", "Ульяна", 100.0, "RUB"))
    display_col.add(SavingsAccount("8749285023", "Светлана", 200.0, "USD", 0.01))
    
    print("Вызов display() для каждого элемента в display_col:")
    for item in display_col:
        print(f"  результат: {item.display()}")
        
    # 3.2 Protocol Scorable
    score_col: TypedCollection[Scorable] = TypedCollection()
    score_col.add(BankAccount("1234567890", "Виктория", 1000.0, "RUB")) # score() = balance
    score_col.add(CreditAccount("2345678901", "Бедолага", 0.0, "RUB", 50000, 0.1)) # score() = credit_limit
    score_col.add(SavingsAccount("3456789012", "Светлана", 1000.0, "RUB", 0.1)) # score() = balance + interest
    
    print("\nРасчет score() для Scorable объектов:")
    for item in score_col:
        print(f"  Владелец: {item.owner if hasattr(item, 'owner') else 'Неизвестный'}, score: {item.score()}")

if __name__ == "__main__":
    main()
