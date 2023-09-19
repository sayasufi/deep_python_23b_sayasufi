"""
Задание 2
Функция генератора для чтения и фильтрации файла
"""

import os
import io


def gen_search_words(file_object, search_words):
    """Функция генератора для чтения и фильтрации файла"""
    # Проверка корректности типов входных данных
    if (
        not isinstance(search_words, list)
        or not isinstance(file_object, (io.IOBase, str))
        or any(not isinstance(n, str) for n in search_words)
    ):
        raise TypeError
    # Проверка того, что объект является файловым объектом
    if isinstance(file_object, str) and not os.path.exists(file_object):
        raise FileNotFoundError
    set_words = set(map(str.lower, search_words))
    # Если объект имеет атрибут name,
    # то возращает значение атрибута, иначе возращает имя файла
    file_name = getattr(file_object, "name", file_object)
    with open(file_name, "r", encoding="UTF-8") as file:
        for line in file:
            if set_words & set(line.lower().split()):
                yield line.strip()
