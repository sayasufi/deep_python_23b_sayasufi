"""
Задание 2
Дескрипторы с проверками типов и значений данных
"""


class Integer:
    """Дескриптор с проверкой на int"""

    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an integer")
        return setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"_int_descr_{name}"


class String:
    """Дескриптор с проверкой на str"""

    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        return setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"_str_descr_{name}"


class PositiveInteger:
    """Дескриптор с проверкой на положительный int"""

    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an integer")
        if value <= 0:
            raise ValueError("Expected a positive integer")
        return setattr(instance, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"_pos_int_descr_{name}"


class Data:
    """Шаблонный класс"""

    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
