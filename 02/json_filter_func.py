"""
Задание 1
"""
import json


def change_word() -> str:
    """Функция, обрабатывающая найденное слово"""


def parse_json(
    json_str: str, required_fields=None, keywords=None, keyword_callback=None
) -> str:
    """Функция, изменяющая json-строку"""
    # Проверяем является ли аргумент строкой
    if not isinstance(json_str, str):
        raise TypeError

    # Если не переданы один из этих аргументов,
    # то ничего менять не надо и сразу выводим не изменившеюся строку
    if any(
        (required_fields is None, keywords is None, keyword_callback is None)
    ):
        return json_str

    # Проверка на тип входных данных, для последней
    # она должна быть функцией, мб другая проверка там будет
    if any(
        (
            not isinstance(required_fields, list),
            not isinstance(keywords, list),
            not callable(keyword_callback),
        )
    ):
        raise TypeError

    if any((not required_fields, not keywords)):
        return json_str

    # Каждый элемент списка должен быть строкой,
    # для функции бы тоже надо добавить проверку, что она возвращает строку
    if any(
        (
            any(not isinstance(word, str) for word in required_fields),
            any(not isinstance(word, str) for word in keywords),
        )
    ):
        raise TypeError

    # Десериализация данных
    try:
        json_doc = json.loads(json_str)
    except json.decoder.JSONDecodeError as exc:
        raise ValueError from exc

    if not isinstance(json_doc, dict):
        raise ValueError

    required_fields = set(map(str.lower, required_fields)) & set(
        map(str.lower, json_doc.keys())
    )

    if not required_fields:
        return json.dumps(json_doc, ensure_ascii=False)
    # Отбираем уникальные слова
    words = set(map(str.lower, keywords))
    # Итерируемся по указанным ключам,
    # мб добавлю проверку, что ключа нет в json-строке
    for key in required_fields:
        verifiable_words = words & set(map(str.lower, json_doc[key].split()))
        if verifiable_words:
            line = json_doc[key].split()

            # Изменяю значение по ключу, если слово есть в списке
            json_doc[key] = " ".join(
                str(keyword_callback(word))
                if word.lower() in verifiable_words
                else word
                for word in line
            )

    # Возвращаю новую строку
    return json.dumps(json_doc, ensure_ascii=False)
