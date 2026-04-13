def validate_owner(value: str):
    if not isinstance(value,str):
        raise TypeError("Владелец должен быть строкой")
    if not value.strip():
        raise ValueError("Имя владельца не может быть пустым")
    
def validate_ID(value: str):
    if not isinstance(value, str):
        raise TypeError("Номер счёта должен быть строкой")
    if len(value) != 10:
        raise ValueError("Номер счёта должен состоять ровно из 10 цифр")
    
def validate_currency(value: str):
    allowed = {"USD","EUR","RUB"}
    if not isinstance(value, str):
        raise TypeError("Валюта должна быть строкой")
    if value.upper() not in allowed:
        raise ValueError(f'Валюта должна быть одной из возможных({allowed})')

def validate_positive(value: float, field_name: str):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} должно быть числом")
    if value < 0:
        raise ValueError(f"{field_name} не может быть отрицательным")