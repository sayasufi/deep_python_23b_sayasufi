"""
Задание 1
Функция, которая в качестве аргументов принимает строку json,
список полей, которые необходимо обработать, список имён,
которые нужно найти и функцию-обработчика имени,
который срабатывает, когда в каком-либо поле было найдено ключевое имя.
"""

import json


def callback() -> str:
    """Функция, обрабатывающая найденное слово"""


def parse_json(
    json_str, required_fields=None, keywords=None, keyword_callback=None
):
    """Функция"""
    if any(
        (required_fields is None, keywords is None, keyword_callback is None)
    ):
        return json_str
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
        return json_str
    # Парсим JSON
    try:
        json_doc = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Некорректный JSON") from exc

    # Обрабатываем каждое поле
    for field in required_fields:
        if field in json_doc:
            value = json_doc[field]
            # Проверяем наличие ключевых имён в значении
            for keyword in keywords:
                if keyword.lower() in value.lower():
                    # Вызываем функцию-обработчик
                    if keyword_callback is not None:
                        new_value = keyword_callback(keyword)
                        # Заменяем найденное слово в значении
                        value = value.replace(keyword, new_value)
            json_doc[field] = value

    return json.dumps(json_doc, ensure_ascii=False)
