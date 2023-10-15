"""
Задание 2
Тесты для дескрипторов
"""

import unittest
from descriptor import Data


class TestData(unittest.TestCase):
    """unittest класс"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_valid(self):
        """Тест валидных значений"""
        data = Data(1, "test", 100)
        self.assertEqual(data.num, 1)
        self.assertEqual(data.name, "test")
        self.assertEqual(data.price, 100)

        data = Data(-100, "", 1)
        self.assertEqual(data.num, -100)
        self.assertEqual(data.name, "")
        self.assertEqual(data.price, 1)

    def test_changing_values_to_valid_invalid(self):
        """Тест валидных значений"""
        data = Data(1, "test", 100)
        self.assertEqual(data.num, 1)
        self.assertEqual(data.name, "test")
        self.assertEqual(data.price, 100)

        with self.assertRaises(TypeError):
            data.num = []
        self.assertEqual(data.num, 1)

        with self.assertRaises(TypeError):
            data.name = 5
        self.assertEqual(data.name, "test")

        with self.assertRaises(ValueError):
            data.price = -10
        self.assertEqual(data.price, 100)

        data.num = 8
        data.name = "example"
        data.price = 50
        self.assertEqual(data.num, 8)
        self.assertEqual(data.name, "example")
        self.assertEqual(data.price, 50)

    def test_num_invalid(self):
        """Тест неверного num"""
        with self.assertRaises(TypeError):
            Data("not an integer", "test", 100)
        with self.assertRaises(TypeError):
            Data(4.53, "test", 100)

    def test_name_invalid(self):
        """Тест неверного name"""
        with self.assertRaises(TypeError):
            Data(1, 100, 100)
        with self.assertRaises(TypeError):
            Data(1, ["test"], 100)

    def test_price_invalid(self):
        """Тест неверного price"""
        with self.assertRaises(ValueError):
            Data(1, "test", -100)
        with self.assertRaises(ValueError):
            Data(1, "test", -1)
        with self.assertRaises(ValueError):
            Data(1, "test", 0)
        with self.assertRaises(TypeError):
            Data(1, "test", "error")

    def test_descriptor_for_class(self):
        """Тест для значений самого класса"""
        self.assertEqual(Data.num, None)
        self.assertEqual(Data.name, None)
        self.assertEqual(Data.price, None)
