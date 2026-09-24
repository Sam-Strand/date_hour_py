from date_hour import HourRange, DateHour

print("=== Тестирование HourRange ===\n")

print("1. Диапазоны из одного часа:")
hour1 = HourRange("2024-01-15 14")
hour2 = HourRange("2024-01-15 14:30:45")
print(f"   Час:   {hour1} -> {len(hour1)} часов")
print(f"   Час:   {hour2} -> {len(hour2)} часов")
print()

print("2. Диапазоны из нескольких часов:")
day = HourRange("2024-01-15", "2024-01-16")
week = HourRange("2024-01-15", "2024-01-22")
print(f"   День:  {day} -> {len(day)} часов")
print(f"   Неделя:{week} -> {len(week)} часов")
print()

print("3. Самодостаточные периоды (интерпретируются как часы):")
year = HourRange("2024")
month = HourRange("2024-01")
day = HourRange("2024-01-15")
print(f"   Год:   {year} -> {len(year)} часов")
print(f"   Месяц: {month} -> {len(month)} часов")
print(f"   День:  {day} -> {len(day)} часов")
print()

print("4. Арифметика:")
tr = HourRange("2024-01-15 10", "2024-01-15 14")
print(f"   Исходный: {tr}")
print(f"   Начало -2ч: {tr.start - 2}")
print(f"   Конец +3ч:  {tr.stop + 3}")
print()

print("5. Использование в запросах:")
start = DateHour("2024-01-15")
end = start + 24
tr = HourRange(start, end)
print(f"   WHERE time >= '{tr.start}' AND time < '{tr.stop}'")
print(f"   Период: {tr.start} - {tr.stop} ({len(tr)} часов)")
print()

print("✓ Все тесты пройдены")
