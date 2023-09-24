"""
Задание 2
Декоратор, который считает среднее время выполнения последних k вызовов.
"""
import time
from functools import wraps


def mean(k):
    """Декоратор, принимающий кол-во вызовов"""
    # Проверка типа передаваемого аргумента
    if not isinstance(k, int):
        raise TypeError

    # k должно быть больше 0
    if k < 1:
        raise ValueError

    def decorator(func):
        """Декоратор, принимающий функцию"""
        # Передается только вызываемый объект
        if not callable(func):
            raise TypeError

        mem = {i: None for i in range(k)}
        counter = 0  # счётчик выполнений

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Функция считающая среднее время выполнения"""
            nonlocal counter
            nonlocal mem

            start = time.perf_counter()  # фиксирую время старта
            func(*args, **kwargs)  # выполняю функцию
            func_time = (
                time.perf_counter() - start
            )  # фиксирую время работы функции
            counter += 1  # добавляю 1 выполнение
            mem[counter % k] = func_time  # меняю значение в кеше

            # проверка на вызов k раз функции
            if None not in mem.values():
                return sum(mem.values()) / k
            return None

        return wrapper

    return decorator
