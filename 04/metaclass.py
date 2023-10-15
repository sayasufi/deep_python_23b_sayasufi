"""
Задание 1
Мета класс, который в начале названий всех атрибутов и методов,
кроме магических, добавляет префикс "custom_
"""

import copy


class CustomMeta(type):
    """Мета класс"""

    @staticmethod
    def create_custom_setattr(cls_obj, key, value):
        """Создание кастомного setattr"""
        if not (
            key.endswith("__") and key.startswith("__")
        ) and not key.startswith("custom_"):
            object.__setattr__(cls_obj, f"custom_{key}", value)
        else:
            object.__setattr__(cls_obj, key, value)

    def __new__(mcs, name, bases, class_dict, **kwargs):
        class_dict_clone = copy.deepcopy(class_dict)
        for attr_name, attr_value in class_dict.items():
            if not (
                attr_name.endswith("__") and attr_name.startswith("__")
            ) and not attr_name.startswith("custom_"):
                class_dict_clone["custom_" + attr_name] = attr_value
                del class_dict_clone[attr_name]

        class_dict_clone["__setattr__"] = mcs.create_custom_setattr
        return super().__new__(mcs, name, bases, class_dict_clone, **kwargs)

    def __setattr__(cls, attr_name, attr_value):
        if not (
            attr_name.endswith("__") and attr_name.startswith("__")
        ) and not attr_name.startswith("custom_"):
            attr_name = "custom_" + attr_name
        super().__setattr__(attr_name, attr_value)
