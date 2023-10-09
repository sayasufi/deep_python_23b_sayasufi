"""
Задание 1
Тесты для мета-класса
"""

import unittest
from metaclass import CustomClass


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
