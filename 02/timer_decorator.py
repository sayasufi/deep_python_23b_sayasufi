"""
Задание 2
Декоратор, который считает среднее время выполнения последних k вызовов.
"""
import time
from functools import wraps


def mean(k):
    """Декоратор, на вход подается кол-во вызовов"""
    # Проверка типа передаваемого аргумента
    if not isinstance(k, int):
        raise TypeError

    # k должно быть больше 0
    if k < 1:
        raise ValueError

    def decorator(func):
        if not callable(func):
            raise TypeError
        execution_times = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_times.append(end_time - start_time)

            if len(execution_times) >= k:
                avg_time = sum(execution_times[-k:]) / k
                print(
                    f"Average execution time of last {k} calls: "
                    f"{avg_time} seconds"
                )
            else:
                avg_time = sum(execution_times) / len(execution_times)
                print(
                    f"Average execution time of last "
                    f"{len(execution_times)} calls: "
                    f"{avg_time} seconds"
                )

            return result

        return wrapper

    return decorator
