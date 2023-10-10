"""
Задание 1
Тестирование функции оценки сообщения
"""

import unittest
from unittest.mock import MagicMock
from message_rating_function import SomeModel, predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    """unittest класс с тестами"""

    def setUp(self):
        print("SETUP")
        self.model = SomeModel()

    def tearDown(self):
        print("TEAR_DOWN")

    def test_neud_when_prediction_less_than_bad_threshold(self):
        """Тесты для неуд"""
        self.model.predict = MagicMock(return_value=0.2)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

    def test_otl_when_prediction_greater_than_good_threshold(self):
        """Тесты для отл"""
        self.model.predict = MagicMock(return_value=0.9)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=1)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

    def test_norm_when_prediction_between_thresholds(self):
        """Тесты для норм"""
        self.model.predict = MagicMock(return_value=0.3)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.4)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.8)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.7)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

    def test_changing_thresholds(self):
        """Тесты для изменяющихся порогов"""
        self.model.predict = MagicMock(return_value=0.2)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.2, good_threshold=1
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.4)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0, good_threshold=0.4
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=1)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=1, good_threshold=1
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=1)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0, good_threshold=0.1
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.9, good_threshold=1
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

    def test_edge_and_near_edge_cases(self):
        """Краевые и около краевые случаи"""

        self.model.predict = MagicMock(return_value=0.299)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.3)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.301)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.799)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.8)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "норм")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.801)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=-0.01)
        self.assertRaises(
            ValueError, predict_message_mood, "Some message", self.model
        )

        self.model.predict = MagicMock(return_value=0)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.01)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "неуд")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=0.99)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=1)
        result = predict_message_mood(
            "Some message", self.model, bad_threshold=0.3, good_threshold=0.8
        )
        self.assertEqual(result, "отл")
        self.assertEqual("Some message", *self.model.predict.call_args.args)

        self.model.predict = MagicMock(return_value=1.01)
        self.assertRaises(
            ValueError, predict_message_mood, "Some message", self.model
        )

    def test_raises_value_error_when_bad_threshold_greater_than_good_threshold(
        self,
    ):
        """Хороший порог ниже плохого"""
        self.assertRaises(
            ValueError,
            predict_message_mood,
            "Some message",
            self.model,
            bad_threshold=0.8,
            good_threshold=0.3,
        )

    def test_raises_predict_error(self):
        """Неверный тип данных функции обработчика"""
        self.model.predict = MagicMock(return_value="dfg")
        self.assertRaises(
            TypeError, predict_message_mood, "Some message", self.model
        )

        self.model.predict = MagicMock(return_value=[0.3])
        self.assertRaises(
            TypeError, predict_message_mood, "Some message", self.model
        )

        self.model.predict = MagicMock(return_value=1.1)
        self.assertRaises(
            ValueError, predict_message_mood, "Some message", self.model
        )

        self.model.predict = MagicMock(return_value=-0.1)
        self.assertRaises(
            ValueError, predict_message_mood, "Some message", self.model
        )

    def test_raises_type_error(self):
        """Неверных тип входных данных"""
        self.assertRaises(TypeError, predict_message_mood, 123, self.model)
        self.assertRaises(
            TypeError,
            predict_message_mood,
            "Some message",
            "Not a SomeModel instance",
        )
        self.assertRaises(
            TypeError,
            predict_message_mood,
            "Some message",
            self.model,
            bad_threshold="ss",
        )
        self.assertRaises(
            TypeError,
            predict_message_mood,
            "Some message",
            self.model,
            good_threshold=[1],
        )

    def test_raises_value_error_when_is_negative(self):
        """Неверные значения порогов, меньше 0"""
        self.assertRaises(
            ValueError,
            predict_message_mood,
            "Some message",
            self.model,
            bad_threshold=-1,
        )
        self.assertRaises(
            ValueError,
            predict_message_mood,
            "Some message",
            self.model,
            good_threshold=-0.1,
        )

    def test_raises_value_error_when_is_more1(self):
        """Неверные значения порогов, больше 1"""
        self.assertRaises(
            ValueError,
            predict_message_mood,
            "Some message",
            self.model,
            bad_threshold=2,
        )
        self.assertRaises(
            ValueError,
            predict_message_mood,
            "Some message",
            self.model,
            good_threshold=1.1,
        )
