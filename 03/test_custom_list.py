"""
Тесты для класса
"""

import unittest

from custom_list import CustomList


def compare_lists(list1, list2):
    """Поэлементное сравнение двух CustomList"""
    if len(list1) != len(list2):
        return False

    for i, list_en in enumerate(list1):
        if list_en != list2[i]:
            return False
    return True


class CustomListTests(unittest.TestCase):
    """Тесты unittest"""

    def test_addition(self):
        """Тест сложения двух CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 9])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5, 6])))

    def test_addition_with_regular_list(self):
        """Тест сложения CustomList и обычного списка"""
        list1 = CustomList([1, 2, 3])
        list2 = [4, 5, 6]
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 9])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, [4, 5, 6]))

    def test_subtraction(self):
        """Тест вычитания двух CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([-3, -3, -3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5, 6])))

    def test_subtraction_with_regular_list(self):
        """Тест вычитания CustomList и обычного списка"""
        list1 = CustomList([1, 2, 3])
        list2 = [4, 5, 6]
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([-3, -3, -3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, [4, 5, 6]))

    def test_addition_different_lengths(self):
        """Тест сложения списков разной длины"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5])))

        list1 = CustomList([4, 5])
        list2 = CustomList([1, 2, 3])
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([4, 5])))
        self.assertTrue(compare_lists(list2, CustomList([1, 2, 3])))

        list1 = CustomList([1, 2, 3])
        list2 = [4, 5]
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5])))

        list1 = [4, 5]
        list2 = CustomList([1, 2, 3])
        result = list1 + list2
        self.assertTrue(compare_lists(result, CustomList([5, 7, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([4, 5])))
        self.assertTrue(compare_lists(list2, CustomList([1, 2, 3])))

    def test_subtraction_different_lengths(self):
        """Тест вычитания списков разной длины"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([-3, -3, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5])))

        list1 = CustomList([4, 5])
        list2 = CustomList([1, 2, 3])
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([3, 3, -3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([4, 5])))
        self.assertTrue(compare_lists(list2, CustomList([1, 2, 3])))

        list1 = [1, 2, 3]
        list2 = CustomList([4, 5])
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([-3, -3, 3])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, [1, 2, 3]))
        self.assertTrue(compare_lists(list2, CustomList([4, 5])))

        list1 = CustomList([1, 2])
        list2 = [4, 5, 6]
        result = list1 - list2
        self.assertTrue(compare_lists(result, CustomList([-3, -3, -6])))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2])))
        self.assertTrue(compare_lists(list2, [4, 5, 6]))

    def test_str_representation(self):
        """Тест переопределенного метода str"""
        list1 = CustomList([1, 2, 3])
        result = str(list1)
        self.assertEqual(result, "[1, 2, 3] (Sum: 6)")

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))

    def test_comparison(self):
        """Тест сравнения CustomList"""
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5, 6])
        self.assertTrue(list1 < list2)
        self.assertFalse(list1 > list2)
        self.assertTrue(list1 == CustomList([1, 2, 3]))
        self.assertFalse(list1 != CustomList([1, 2, 3]))
        self.assertTrue(list2 >= CustomList([4, 5, 6]))
        self.assertTrue(list2 <= CustomList([4, 5, 6]))

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list1, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list2, CustomList([4, 5, 6])))

        list3 = CustomList([1, 2, 3])
        list4 = CustomList([4, 5, 6, 7])
        self.assertTrue(list3 < list4)
        self.assertFalse(list3 == 1)
        self.assertTrue(list3 != "stt")

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list3, CustomList([1, 2, 3])))
        self.assertTrue(compare_lists(list4, CustomList([4, 5, 6, 7])))

        # Тест равенства списков с разными элементами, но одинаковой суммой
        list5 = CustomList([-1, 2, 5])
        list6 = CustomList([0, 3, 3, 0])
        self.assertTrue(list5 == list6)
        self.assertTrue(list5 >= list6)
        self.assertTrue(list5 <= list6)
        self.assertFalse(list5 < list6)
        self.assertFalse(list5 > list6)
        self.assertFalse(list5 != list6)

        # Проверка, что исходные списки остались неизменными
        self.assertTrue(compare_lists(list5, CustomList([-1, 2, 5])))
        self.assertTrue(compare_lists(list6, CustomList([0, 3, 3, 0])))

    def test_error_handling(self):
        """Тест обработки ошибок"""
        with self.assertRaises(TypeError):
            CustomList([1, 2, "3"])  # Недопустимый элемент в списке

        self.assertRaises(
            TypeError, lambda: CustomList([1, 2, 3]) + "not a list"
        )

        self.assertRaises(TypeError, lambda: 1 + CustomList([1, 2, 3]))

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) - 1)

        self.assertRaises(TypeError, lambda: 1 - CustomList([1, 2, 3]))

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) < 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) > 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) >= 1)

        self.assertRaises(TypeError, lambda: CustomList([1, 2, 3]) <= 1)
