"""
Задание 1
Тесты для мета-класса
"""

import unittest
from metaclass import CustomMeta


class CustomClass(metaclass=CustomMeta):
    """Наследуемый класс"""

    x = 50
    _m = 0
    __mp = 0  # pylint: disable=unused-private-member

    def __init__(self, val=99):
        self.val = val
        self._n = 0
        self.__np = 0  # pylint: disable=unused-private-member

    def line(self):
        """Функция возвращающая 100"""
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestCustomClass(unittest.TestCase):
    """unittest class"""

    def test_attribute_prefix(self):
        """Test that non-magic attributes have the "custom_" prefix added"""
        custom_class = CustomClass()
        self.assertTrue(hasattr(custom_class, "custom_x"))
        self.assertEqual(getattr(custom_class, "custom_x"), 50)
        self.assertTrue(hasattr(custom_class, "custom_val"))
        self.assertEqual(getattr(custom_class, "custom_val"), 99)
        self.assertFalse(hasattr(custom_class, "x"))
        self.assertFalse(hasattr(custom_class, "val"))

    def test_method_prefix(self):
        """Test that non-magic methods have the "custom_" prefix added"""
        custom_class = CustomClass()
        self.assertTrue(hasattr(custom_class, "custom_line"))
        self.assertFalse(hasattr(custom_class, "line"))
        line_func = getattr(custom_class, "custom_line")
        self.assertEqual(line_func(), 100)
        self.assertEqual(str(custom_class), "Custom_by_metaclass")

    def test_class_attribute(self):
        """Test that class attributes are modified with the "custom_" prefix"""
        self.assertTrue(hasattr(CustomClass, "custom_x"))
        self.assertFalse(hasattr(CustomClass, "x"))
        self.assertEqual(getattr(CustomClass, "custom_x"), 50)

        self.assertTrue(hasattr(CustomClass, "custom_line"))
        self.assertFalse(hasattr(CustomClass, "line"))
        line_func = getattr(CustomClass, "custom_line")
        self.assertEqual(line_func(self), 100)

    def test_instance_attribute(self):
        """Test that instance attributes added after
        initialization are modified with the "custom_" prefix"""
        custom_class = CustomClass()
        custom_class.dynamic = True
        self.assertTrue(hasattr(custom_class, "custom_dynamic"))
        self.assertFalse(hasattr(custom_class, "dynamic"))
        self.assertEqual(getattr(custom_class, "custom_dynamic"), True)

        custom_class.y = "test"
        self.assertTrue(hasattr(custom_class, "custom_y"))
        self.assertFalse(hasattr(custom_class, "y"))
        self.assertEqual(getattr(custom_class, "custom_y"), "test")

        CustomClass.y = "test1"
        self.assertTrue(hasattr(CustomClass, "custom_y"))
        self.assertFalse(hasattr(CustomClass, "y"))
        self.assertEqual(getattr(CustomClass, "custom_y"), "test1")

        custom_class.x = [100]
        self.assertTrue(hasattr(custom_class, "custom_x"))
        self.assertFalse(hasattr(custom_class, "x"))
        self.assertEqual(getattr(custom_class, "custom_x"), [100])

        custom_class.line = "30"
        self.assertTrue(hasattr(custom_class, "custom_line"))
        self.assertFalse(hasattr(custom_class, "line"))
        line_func = getattr(custom_class, "custom_line")
        self.assertEqual(line_func, "30")

        custom_class.__test__ = 10
        self.assertTrue(hasattr(custom_class, "__test__"))
        self.assertFalse(hasattr(custom_class, "custom___test__"))
        self.assertEqual(getattr(custom_class, "__test__"), 10)

    def test_instance_attribute_existing_pr(self):
        """Test for existing _protected and __private attributes"""
        custom_class = CustomClass()

        self.assertTrue(hasattr(CustomClass, "custom__m"))
        self.assertFalse(hasattr(CustomClass, "_m"))
        self.assertEqual(getattr(CustomClass, "custom__m"), 0)

        self.assertTrue(hasattr(CustomClass, "custom__CustomClass__mp"))
        self.assertFalse(hasattr(CustomClass, "_CustomClass__mp"))
        self.assertEqual(getattr(CustomClass, "custom__CustomClass__mp"), 0)

        self.assertTrue(hasattr(custom_class, "custom__n"))
        self.assertFalse(hasattr(custom_class, "_n"))
        self.assertEqual(getattr(custom_class, "custom__n"), 0)

        self.assertTrue(hasattr(custom_class, "custom__CustomClass__np"))
        self.assertFalse(hasattr(custom_class, "_CustomClass__np"))
        self.assertEqual(getattr(custom_class, "custom__CustomClass__np"), 0)

    def test_instance_attribute_add_pr(self):
        """Test for add _protected and __private attributes"""
        custom_class = CustomClass()

        custom_class._protected = 33  # pylint: disable=W0212
        self.assertTrue(hasattr(custom_class, "custom__protected"))
        self.assertFalse(hasattr(custom_class, "_protected"))
        self.assertEqual(getattr(custom_class, "custom__protected"), 33)

        CustomClass._protected_class = -1  # pylint: disable=W0212
        self.assertTrue(hasattr(CustomClass, "custom__protected_class"))
        self.assertFalse(hasattr(CustomClass, "_protected_class"))
        self.assertEqual(getattr(CustomClass, "custom__protected_class"), -1)

    def test_change_attribute(self):
        """Test for change attribute"""
        custom_class = CustomClass()

        custom_class.test = 0
        self.assertTrue(hasattr(custom_class, "custom_test"))
        self.assertFalse(hasattr(custom_class, "test"))
        self.assertEqual(getattr(custom_class, "custom_test"), 0)

        custom_class.custom_test = 2
        self.assertTrue(hasattr(custom_class, "custom_test"))
        self.assertFalse(hasattr(custom_class, "custom_custom_test"))
        self.assertEqual(getattr(custom_class, "custom_test"), 2)

        CustomClass.test_class = 0
        self.assertTrue(hasattr(custom_class, "custom_test_class"))
        self.assertFalse(hasattr(custom_class, "test_class"))
        self.assertEqual(getattr(custom_class, "custom_test_class"), 0)

        CustomClass.custom_test_class = 2
        self.assertTrue(hasattr(custom_class, "custom_test_class"))
        self.assertFalse(hasattr(custom_class, "custom_custom_test_class"))
        self.assertEqual(getattr(custom_class, "custom_test_class"), 2)

    def test_attribute_error(self):
        """Test for attribute error"""
        custom_class = CustomClass()
        CustomClass.y = "test"
        custom_class.dynamic = True
        with self.assertRaises(AttributeError):
            print(CustomClass.y)
        with self.assertRaises(AttributeError):
            print(custom_class.dynamic)
        with self.assertRaises(AttributeError):
            print(custom_class.line())
        with self.assertRaises(AttributeError):
            print(CustomClass.line)
