"""
Задание 2
Функция генератора для чтения и фильтрации файла
"""

import os
import io


def gen_search_words(file_object, search_words):
    """Функция генератора для чтения и фильтрации файла"""
    # Проверка корректности типов входных данных
    if not isinstance(file_object, str) and not isinstance(
        file_object, io.IOBase
    ):
        raise TypeError(
            "Invalid file input. Expected a file name or file object."
        )
    if isinstance(file_object, str):
        if not os.path.exists(file_object):
            raise FileNotFoundError
    if not isinstance(search_words, list):
        raise TypeError(
            "Invalid search words input. Expected a list of words."
        )
    for i in search_words:
        if not isinstance(i, str):
            raise TypeError("Invalid search words input. Expected str.")

    if isinstance(file_object, io.IOBase):
        file = file_object
    else:
        file = open(file_object, "r", encoding="UTF-8")

    set_words = set(map(lambda x: x.lower(), search_words))

    with file:
        for line in file:
            if set_words & set(line.lower().split()):
                yield line.strip()
