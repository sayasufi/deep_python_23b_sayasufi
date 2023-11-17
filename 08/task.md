# Домашнее задание advance #05 (память, профилирование)

### 1. Сравнение использования weakref и слотов
Нужно придумать свои типы с несколькими атрибутами:
- класс с обычными атрибутами
- класс со слотами
- класс с атрибутами weakref

Для каждого класса создается большое число экземпляров и замеряется (сравнивается):
- время создания пачки экземпляров
- время доступа/изменения/удаления атрибутов

Результаты оформляются скриншотами c описанием.

### 2. Профилирование
Провести профилирование вызовов и памяти для кода из пункта 1.

Результаты оформляются скриншотами c описанием.

### 3. Декоратор для профилирования
Применение декоратора к функции должно выполнять прoфилирование вызовов (cProfile) всех запусков данной функции.
Вызов метода `.print_stat()` должен выводить единую таблицу со статистикой профилирования суммарно по всем запускам.


```py
def profile_deco():
    ...


@profile_deco
def add(a, b):
    return a + b

@profile_deco
def sub(a, b):
    return a - b

add(1, 2)
add(4, 5)

add.print_stat()  # выводится таблица с результатами профилирования суммарно по всем запускам
```

### 4. Тесты не нужны

### 5. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black