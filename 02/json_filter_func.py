"""
Задание 1
Функция, которая в качестве аргументов принимает строку json,
список полей, которые необходимо обработать, список имён,
которые нужно найти и функцию-обработчика имени,
который срабатывает, когда в каком-либо поле было найдено ключевое имя.
"""

import json


def callback(field, word):
    """Функция, обрабатывающая найденное слово"""
    print(f"Keyword '{word}' was found in field '{field}'")


def parse_json(
    json_str, required_fields=None, keywords=None, keyword_callback=None
):
    """Функция"""
    if any(
        (required_fields is None, keywords is None, keyword_callback is None)
    ):
        return
    # Проверяем аргументы на типы
    if not isinstance(json_str, str):
        raise TypeError("json_str должен быть строкой")
    if not isinstance(required_fields, list):
        raise TypeError("required_fields должен быть списком")
    if not isinstance(keywords, list):
        raise TypeError("keywords должен быть списком")

    if not callable(keyword_callback):
        raise TypeError("keyword_callback должен быть функцией")

    if not required_fields or not keywords:
        return
    # Парсим JSON
    try:
        json_doc = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Некорректный JSON") from exc

    # Обрабатываем каждое поле
    for field in required_fields:
        if field in json_doc:
            # Проверяем наличие ключевых имён в значении
            for keyword in keywords:
                if keyword.lower() in json_doc[field].lower().split():
                    keyword_callback(field, keyword)
