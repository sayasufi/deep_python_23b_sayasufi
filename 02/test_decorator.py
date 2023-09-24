"""
Задание 2
Тесты для декоратора
"""

import unittest
from unittest import mock
from timer_decorator import mean


class TestDecorator(unittest.TestCase):
    """Unittest класс с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_average_execution_time(self):
        """Проверка валидных данных"""
        with mock.patch("timer_decorator.time.perf_counter") as mock_fetch:
            mock_fetch.side_effect = (0, 1, 0, 1, 0, 1, 0, 10)

            @mean(3)
            def my_function():
                pass

            for i in range(2):
                self.assertEqual(my_function(), None)

            self.assertEqual(my_function(), 1)
            self.assertEqual(my_function(), 4)
            self.assertEqual(mock_fetch.call_count, 8)
            self.assertEqual(
                my_function.__name__, "my_function"
            )  # Function name is preserved
            self.assertEqual(
                my_function.__doc__, None
            )  # Function docstring is preserved

        with mock.patch("timer_decorator.time.perf_counter") as mock_fetch:
            mock_fetch.side_effect = (0, 2, 0, 2, 0, 2)

            @mean(1)
            def my_function1():
                pass

            for i in range(3):
                self.assertEqual(my_function1(), 2)

            self.assertEqual(mock_fetch.call_count, 6)

        with mock.patch("timer_decorator.time.perf_counter") as mock_fetch:
            mock_fetch.side_effect = [0 if i < 80 else i for i in range(100)]

            @mean(10)
            def my_function2():
                pass

            for _ in range(9):  # 50 - 9 = 41
                self.assertEqual(my_function2(), None)

            for _ in range(31):  # 41 - 31 = 10
                self.assertEqual(my_function2(), 0)

            for _ in range(9):  # 10 - 9 = 1
                my_function2()

            # Последний прогон
            self.assertEqual(my_function2(), 1)
            self.assertEqual(mock_fetch.call_count, 100)

    def test_invalid_incorrect_data_type(self):
        """Проверка ошибки TypeError"""
        self.assertRaises(TypeError, mean, "")
        self.assertRaises(TypeError, mean(5), 5)

    def test_invalid_incorrect_data(self):
        """Проверка ошибки ValueError"""
        self.assertRaises(ValueError, mean, 0)
        self.assertRaises(ValueError, mean, -1)
