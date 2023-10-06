"""
Задание 1
Функция оценки сообщения
"""


class SomeModel:
    """Класс модели"""

    def predict(self, message: str) -> float:
        """Функция возращающая от 0 до 1"""

    def another_method(self):
        """
        Вторая функция, чтобы не ругался pylint
        """


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_threshold: float = 0.3,
    good_threshold: float = 0.8,
) -> str:
    """Функция оценки"""
    if not isinstance(message, str):
        raise TypeError("message должен быть строкой")
    if not isinstance(model, SomeModel):
        raise TypeError("model должен быть экземпляром класса SomeModel")
    if not isinstance(bad_threshold, (float, int)) or not isinstance(
        good_threshold, (float, int)
    ):
        raise TypeError(
            "bad_threshold и good_threshold "
            "должны быть числами с плавающей точкой"
        )
    if bad_threshold < 0 or good_threshold < 0:
        raise ValueError(
            "bad_threshold и good_threshold должны быть положительными числами"
        )
    if bad_threshold > 1 or good_threshold > 1:
        raise ValueError("bad_threshold и good_threshold должны быть меньше 1")
    if bad_threshold > good_threshold:
        raise ValueError(
            "bad_threshold должен быть меньше, чем good_threshold"
        )

    prediction = model.predict(message)
    if not isinstance(prediction, (float, int)):
        raise TypeError("prediction должно быть числом с плавающей точкой")
    if prediction > 1 or prediction < 0:
        raise ValueError

    if prediction < bad_threshold:
        return "неуд"
    if prediction > good_threshold:
        return "отл"
    return "норм"
