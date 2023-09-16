from model import SomeModel


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    # Проверка корректности типа данных модели
    if not isinstance(model, SomeModel):
        raise TypeError

    prediction = model.predict(message)

    # Проверка корректности типов входных данных
    if any((not isinstance(prediction, (float, int)), not isinstance(message, str),
            not isinstance(bad_thresholds, (float, int)), not isinstance(good_thresholds, (float, int)))):
        raise TypeError

    # Проверка корректности значений входных данных
    if any((not bad_thresholds <= good_thresholds, not 0 <= bad_thresholds <= 1, not 0 <= good_thresholds <= 1)):
        raise ValueError

    if 0 <= prediction < bad_thresholds:
        return "неуд"
    elif 1 >= prediction > good_thresholds:
        return "отл"
    elif bad_thresholds <= prediction <= good_thresholds:
        return "норм"
    else:
        raise ValueError

