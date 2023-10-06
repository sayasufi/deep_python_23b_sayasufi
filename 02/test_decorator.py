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
        mock_print = mock.Mock()
        with mock.patch("timer_decorator.time.time") as mock_fetch, mock.patch(
            "builtins.print", mock_print
        ):
            mock_fetch.side_effect = (0, 1, 0, 1, 0, 1, 0, 10)

            @mean(3)
            def function1():
                pass

            for i in range(3):
                function1()

            self.assertEqual(
                mock_print.call_args[0][0],
                "Average execution time of last 3 calls: 1.0 seconds",
            )
            function1()
            self.assertEqual(
                mock_print.call_args[0][0],
                "Average execution time of last 3 calls: 4.0 seconds",
            )
            self.assertEqual(mock_fetch.call_count, 8)
            self.assertEqual(
                function1.__name__, "function1"
            )  # Function name is preserved
            self.assertEqual(
                function1.__doc__, None
            )  # Function docstring is preserved

            mock_fetch.side_effect = (0, 2, 0, 2, 0, 2)

            @mean(1)
            def function2():
                pass

            for i in range(3):
                function2()
                self.assertEqual(
                    mock_print.call_args[0][0],
                    "Average execution time of last 1 calls: 2.0 seconds",
                )

            self.assertEqual(mock_fetch.call_count, 6 + 8)

            mock_fetch.side_effect = [0 if i < 80 else i for i in range(100)]

            @mean(10)
            def function3():
                pass

            for i in range(9):  # 50 - 9 = 41
                function3()
                self.assertEqual(
                    mock_print.call_args[0][0],
                    f"Average execution time of last {i + 1} calls: "
                    f"0.0 seconds",
                )

            for _ in range(31):  # 41 - 31 = 10
                function3()
                self.assertEqual(
                    mock_print.call_args[0][0],
                    "Average execution time of last 10 calls: 0.0 seconds",
                )

            for _ in range(10):  # 10 - 9 = 1
                function3()
            self.assertEqual(
                mock_print.call_args[0][0],
                "Average execution time of last 10 calls: 1.0 seconds",
            )

            self.assertEqual(mock_fetch.call_count, 100 + 6 + 8)

    def test_invalid_incorrect_data_type(self):
        """Проверка ошибки TypeError"""
        self.assertRaises(TypeError, mean, "")
        self.assertRaises(TypeError, mean(5), 5)

    def test_invalid_incorrect_data(self):
        """Проверка ошибки ValueError"""
        self.assertRaises(ValueError, mean, 0)
        self.assertRaises(ValueError, mean, -1)
