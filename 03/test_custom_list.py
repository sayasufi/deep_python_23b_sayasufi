"""
Тесты для класса
"""

import unittest
from custom_list import CustomList


class CustomListTests(unittest.TestCase):
    """Тесты unittest"""

    def test_addition(self):
        """Тест сложения двух CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 9]))

    def test_addition_with_regular_list(self):
        """Тест сложения CustomList и обычного списка"""
        list1 = CustomList([1, 2, 3])
        list2 = [4, 5, 6]
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 9]))

    def test_subtraction(self):
        """Тест вычитания двух CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        result = list1 - list2
        self.assertEqual(result, CustomList([-3, -3, -3]))

    def test_subtraction_with_regular_list(self):
        """Тест вычитания CustomList и обычного списка"""
        list1 = CustomList([1, 2, 3])
        list2 = [4, 5, 6]
        result = list1 - list2
        self.assertEqual(result, CustomList([-3, -3, -3]))

    def test_addition_different_lengths(self):
        """Тест сложения списков разной длины"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 3]))

        list1 = CustomList([4, 5])
        list2 = CustomList([1, 2, 3])
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 3]))

        list1 = CustomList([1, 2, 3])
        list2 = [4, 5]
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 3]))

        list1 = [4, 5]
        list2 = CustomList([1, 2, 3])
        result = list1 + list2
        self.assertEqual(result, CustomList([5, 7, 3]))

    def test_subtraction_different_lengths(self):
        """Тест вычитания списков разной длины"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        result = list1 - list2
        self.assertEqual(result, CustomList([-3, -3, 3]))

        list1 = CustomList([4, 5])
        list2 = CustomList([1, 2, 3])
        result = list1 - list2
        self.assertEqual(result, CustomList([3, 3, -3]))

        list1 = [1, 2, 3]
        list2 = CustomList([4, 5])
        result = list1 - list2
        self.assertEqual(result, CustomList([-3, -3, 3]))

        list1 = CustomList([1, 2])
        list2 = [4, 5, 6]
        result = list1 - list2
        self.assertEqual(result, CustomList([-3, -3, -6]))

    def test_str_representation(self):
        """Тест переопределенного метода str"""
        list1 = CustomList([1, 2, 3])
        result = str(list1)
        self.assertEqual(result, "[1, 2, 3] (Sum: 6)")

    def test_comparison(self):
        """Тест сравнения CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        self.assertTrue(list1 < list2)
        self.assertTrue([1, 2, 3] < list2)
        self.assertFalse(list1 > list2)
        self.assertTrue([4, 5, 6] > list1)
        self.assertTrue(list1 == CustomList([1, 2, 3]))
        self.assertTrue([1, 2, 3] == CustomList([1, 2, 3]))
        self.assertFalse(list1 != CustomList([1, 2, 3]))
        self.assertTrue(list2 >= CustomList([4, 5, 6]))
        self.assertTrue([4, 5, 6] >= list1)
        self.assertTrue(list2 <= CustomList([4, 5, 6]))
        self.assertTrue([1, 2, 3] <= list2)

        list3 = CustomList([1, 2, 3])
        list4 = CustomList([4, 5, 6, 7])
        self.assertTrue(list3 < list4)
        self.assertFalse(list3 == 1)
        self.assertTrue(list3 != "stt")

    def test_error_handling(self):
        """Тест обработки ошибок"""
        with self.assertRaises(TypeError):
            CustomList([1, 2, "3"])  # Недопустимый элемент в списке

        self.assertRaises(
            TypeError, lambda: CustomList([1, 2, 3]) + "not a list"
        )

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) - 1)

        self.assertRaises(TypeError, lambda: 1 - CustomList([1, 2, 3]))

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) < 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) > 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) >= 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) <= 1)
