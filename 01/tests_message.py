"""
Задание 1
Тестирование функции оценки сообщения
"""

import unittest
from unittest import mock

from model import SomeModel
from message_rating_function import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    """unittest класс с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    # Тест 1
    def test_norm(self):
        """
        Проверка валидных данных,
        при данных функции predict, получаем норм
        """
        # Мокаем функцию, подменяя выходные данные
        with mock.patch("message_rating_function.SomeModel.predict") \
                as mock_fetch:
            mock_fetch.side_effect = [0.4, 0.3, 0.8]
            self.assertEqual("норм", predict_message_mood("", SomeModel()))
            self.assertEqual("норм", predict_message_mood("", SomeModel()))
            self.assertEqual("норм", predict_message_mood("", SomeModel()))

    # Тест 2
    def test_otl(self):
        """
        Проверка валидных данных,
        при данных функции predict, получаем отл
        """
        with mock.patch("message_rating_function.SomeModel.predict") \
                as mock_fetch:
            mock_fetch.side_effect = [0.9, 1]
            self.assertEqual("отл", predict_message_mood("", SomeModel()))
            self.assertEqual("отл", predict_message_mood("", SomeModel()))

    # Тест 3
    def test_udovl(self):
        """
        Проверка валидных данных,
        при данных функции predict, получаем неуд
        """
        with mock.patch("message_rating_function.SomeModel.predict") \
                as mock_fetch:
            mock_fetch.side_effect = [0.2, 0]
            self.assertEqual("неуд", predict_message_mood("", SomeModel()))
            self.assertEqual("неуд", predict_message_mood("", SomeModel()))

    # Тест 4
    def test_invalid_input_data(self):
        """
        Проверка ошибки ValueError,
        если передаваемые значения выходят за границы
        """
        with mock.patch("message_rating_function.SomeModel.predict") \
                as mock_fetch:
            mock_fetch.side_effect = [3, -1, 0.4, 1, 1]
            self.assertRaises(ValueError, predict_message_mood,
                              '', SomeModel())
            self.assertRaises(ValueError, predict_message_mood,
                              '', SomeModel())
            self.assertRaises(ValueError, predict_message_mood,
                              '', SomeModel(), bad_thresholds=1,
                              good_thresholds=0.5)
            self.assertRaises(ValueError, predict_message_mood,
                              '', SomeModel(), bad_thresholds=-1,
                              good_thresholds=0.5)
            self.assertRaises(ValueError, predict_message_mood,
                              '', SomeModel(), bad_thresholds=0.5,
                              good_thresholds=4)

    # Тест 5
    def test_incorrect_data_type(self):
        """
        Проверка ошибки TypeError,
        если передаваемые значения не удовлетворяют типу данных
        """
        with mock.patch("message_rating_function.SomeModel.predict") \
                as mock_fetch:
            mock_fetch.side_effect = ['3', 'ddd', 1, 1, 1, 1, 1]
            self.assertRaises(TypeError, predict_message_mood,
                              '', SomeModel())
            self.assertRaises(TypeError, predict_message_mood,
                              '', SomeModel())
            self.assertRaises(TypeError, predict_message_mood,
                              1, SomeModel())
            self.assertRaises(TypeError, predict_message_mood,
                              '', {})
            self.assertRaises(TypeError, predict_message_mood,
                              '', SomeModel(), bad_thresholds='')
            self.assertRaises(TypeError, predict_message_mood,
                              '', SomeModel(), good_thresholds=[1])
            self.assertRaises(TypeError, predict_message_mood,
                              '', SomeModel(), 1, bad_thresholds=0.3,
                              good_thresholds=0.8)