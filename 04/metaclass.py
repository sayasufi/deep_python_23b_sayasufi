"""
Задание 1
Мета класс, который в начале названий всех атрибутов и методов,
кроме магических, добавляет префикс "custom_
"""

import copy


class CustomMeta(type):
    """Мета класс"""

    def __new__(mcs, name, bases, classdict):
        classdict_clone = copy.deepcopy(classdict)
        for attr_name, attr_value in classdict.items():
            if not attr_name[:2] + attr_name[
                -2:
            ] == "____" and not attr_name.startswith("custom_"):
                classdict_clone["custom_" + attr_name] = attr_value
                del classdict_clone[attr_name]
        return super().__new__(mcs, name, bases, classdict_clone)

    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def __setattr__(cls, attr_name, attr_value):
        if not attr_name[:2] + attr_name[-2:] == "____":
            attr_name = "custom_" + attr_name
        super().__setattr__(attr_name, attr_value)


class CustomClass(metaclass=CustomMeta):
    """Наследуемый класс"""

    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        """Функция возвращающая 100"""
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

    def __setattr__(self, attr_name, attr_value):
        if not attr_name[:2] + attr_name[
            -2:
        ] == "____" and not attr_name.startswith("custom_"):
            attr_name = "custom_" + attr_name
        self.__dict__[attr_name] = attr_value
