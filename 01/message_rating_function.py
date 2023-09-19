"""
Задание 1
Функция оценки сообщения
"""

from model import SomeModel


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """Возвращает оценку в зависимости от результата выполнения предсказания
    модели."""
    # Проверка корректности типа данных модели
    if not isinstance(model, SomeModel) or not isinstance(message, str):
        raise TypeError

    prediction = model.predict(message)

    # Проверка корректности типов входных данных
    if any(
        (
            not isinstance(prediction, (float, int)),
            not isinstance(bad_thresholds, (float, int)),
            not isinstance(good_thresholds, (float, int)),
        )
    ):
        raise TypeError

    # Проверка корректности значений входных данных
    if any(
        (
            bad_thresholds > good_thresholds,
            not 0 <= bad_thresholds <= 1,
            not 0 <= good_thresholds <= 1,
        )
    ):
        raise ValueError

    if 0 <= prediction < bad_thresholds:
        return "неуд"
    if 1 >= prediction > good_thresholds:
        return "отл"
    if bad_thresholds <= prediction <= good_thresholds:
        return "норм"
    raise ValueError
