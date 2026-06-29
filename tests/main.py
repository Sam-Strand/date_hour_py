from date_hour import DateHour
from datetime import datetime

print("=== Тестирование DateHour ===")
print()

# Тест 1: Создание из разных форматов
print("1. Создание из разных форматов:")
test_cases = [
    ("2024", "Год"),
    ("2024-01", "Месяц"),
    ("2024-01-15", "День"),
    ("2024-01-15 14", "Час"),
    ("2024-01-15T14:30", "Время с минутами"),
    ("2024-01-15 14:30:45", "Полное время"),
    (datetime(2024, 1, 15, 14, 30, 45), "datetime объект"),
]

for value, desc in test_cases:
    dh = DateHour(value)
    print(f"  {desc:20} -> {dh}")

print()

# Тест 2: Арифметика
print("2. Арифметические операции:")
base = DateHour("2024-01-15 14:30:00")
print(f"  Исходный:        {base}")
print(f"  + 2 часа:        {base + 2}")
print(f"  - 3 часа:        {base - 3}")
print(f"  + 24 часа (сутки): {base + 24}")
print()

# Тест 3: Создание диапазонов
print("3. Создание диапазонов:")
now = DateHour(datetime.now())
print(f"  Сейчас:          {now}")
print(f"  Вчера:           {now - 24} -> {now}")
print(f"  Неделя:          {now - 168} -> {now}")
print()

# Тест 4: Сравнение
print("4. Сравнение:")
dh1 = DateHour("2024-01-15 14")
dh2 = DateHour("2024-01-15 15")
dh3 = DateHour("2024-01-15 14:30")

print(f"  {dh1} == {dh3} -> {dh1 == dh3}")
print(f"  {dh1} < {dh2}  -> {dh1 < dh2}")
print(f"  {dh2} > {dh1}  -> {dh2 > dh1}")
print()

# Тест 5: Использование в запросах
print("5. Использование в запросах к БД:")
start = DateHour("2024-01-15")
end = start + 24  # следующий день

print(f"  WHERE time >= '{start}' AND time < '{end}'")
print(f"  Период: {start} - {end} (всего {int((end._get_datetime() - start._get_datetime()).total_seconds() / 3600)} часов)")
print()

print("✓ Все тесты пройдены")
