"""
Задание 2
Функция генератора для чтения и фильтрации файла
"""

import os
import io


def gen_search_words(file_object, search_words):
    """Функция генератора для чтения и фильтрации файла"""
    # Проверка корректности типов входных данных
    if not isinstance(search_words, list) \
            or not isinstance(file_object, (io.IOBase, str)) \
            or any(not isinstance(n, str) for n in search_words):
        raise TypeError
    # Проверка того, что объект является файловым объектом
    if hasattr(file_object, "close"):
        for line in file_object:
            if set(map(str.lower, search_words)) & set(line.lower().split()):
                yield line.strip()
    else:
        # Проверка того, что файл существует
        if not os.path.exists(file_object):
            raise FileNotFoundError
        with open(file_object, 'r', encoding='UTF-8') as file:
            for line in file:
                if set(map(str.lower, search_words)) \
                        & set(line.lower().split()):
                    yield line.strip()
