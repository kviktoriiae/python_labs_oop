from model import BankAccount


def main():
    # Создание банковского счета
    print("Создание счета:")

    acc1 = BankAccount("1234567890","Виктория Кузина",1000,"USD",500)
    print(acc1)
    
    # Проверка равенства счетов
    print("Проверка равенства:")

    # Создаем второй счет с тем же номером
    acc2 = BankAccount("1234567890","Иван Иванов",200,"USD")

    # Сравнение методом __eq__()
    print("Счета равны:", acc1 == acc2)
    
    # Пополнение счета
    print("Пополнение счета:")
    acc1.deposit(800)
    print(acc1)
    
    # Снятие средств с учетом овердрафта
    print("Снятие средств:")
    acc1.withdraw(1500)
    print(acc1)
    
    # Демонстрация ограничения (ошибка)
    print("Попытка превысить лимит:")

    try:
        acc1.withdraw(1000)
    except ValueError as e:
        print("Ошибка:", e)
        
    # Изменение владельца через setter
    print("Изменение владельца")
    acc1.owner = "Петр Иванов"
    print(acc1)
    
    # Закрытие счета
    print("Закрытие счета:")

    acc1.close()
    print(acc1)

    # Попытка выполнить операцию после закрытия
    try:
        acc1.deposit(100)
    except RuntimeError as e:
        print("Ошибка:", e)
    
    # Пример некорректного создания счета
    print("Ошибка при создании счета")
    try:
        bad_account = BankAccount("123", "", -5000, "BTC")
    except Exception as e:
        print("Ошибка создания:", e)
        
    # Демонстрация атрибута класса
    print("Атрибут класса")
    print("Через класс:", BankAccount.name)
    print("Через объект:", acc1.name)

if __name__ == "__main__":
    main()