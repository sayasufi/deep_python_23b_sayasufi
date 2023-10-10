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
        if not (key.endswith("__") and key.startswith("__")):
            # __private и _protected атрибуты
            if key.startswith("_"):
                object.__setattr__(cls_obj, f"_custom_{key[1:]}", value)
            else:
                object.__setattr__(cls_obj, f"custom_{key}", value)
        else:
            object.__setattr__(cls_obj, key, value)

    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def __new__(mcs, name, bases, class_dict, **kwargs):
        class_dict_clone = copy.deepcopy(class_dict)
        for attr_name, attr_value in class_dict.items():
            if not (attr_name.endswith("__") and attr_name.startswith("__")):
                # __private и _protected атрибуты
                if attr_name.startswith("_"):
                    class_dict_clone[f"_custom_{attr_name[1:]}"] = attr_value
                    del class_dict_clone[attr_name]

                else:
                    class_dict_clone["custom_" + attr_name] = attr_value
                    del class_dict_clone[attr_name]

        class_dict_clone["__setattr__"] = mcs.create_custom_setattr
        return super().__new__(mcs, name, bases, class_dict_clone, **kwargs)

    def __setattr__(cls, attr_name, attr_value):
        if not (attr_name.endswith("__") and attr_name.startswith("__")):
            # __private и _protected атрибуты
            if attr_name.startswith("_"):
                attr_name = f"_custom_{attr_name[1:]}"
            else:
                attr_name = "custom_" + attr_name
        super().__setattr__(attr_name, attr_value)
