"""
Задание 1
Реализовать LRU Cache
"""


class LRUCache:
    """Класс LRUCache"""

    def __init__(self, limit=10):
        if not isinstance(limit, int):
            raise TypeError
        if limit <= 0:
            raise ValueError
        self._value_storage = {}
        self._limit = limit

    def get(self, key):
        """Функция для получения значений"""
        if key in self._value_storage:
            value = self._value_storage.get(key)
            del self._value_storage[key]
            self._value_storage[key] = value
            return value
        return None

    def set(self, key, value):
        """Функция для установки значения"""
        if key in self._value_storage:
            del self._value_storage[key]

        self._insert_item(key, value)
        self._pop_items()

    def change_limit(self, limit):
        """Функция для изменения размера кэша"""
        self._limit = limit
        self._pop_items()

    def _pop_items(self):
        """Функция для удаления элементов"""
        while len(self._value_storage) > self._limit:
            key = next(iter(self._value_storage))
            del self._value_storage[key]

    def _insert_item(self, key, value):
        """Функция для установки значений в словарь"""
        self._value_storage[key] = value

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __str__(self):
        return str(self._value_storage)

    def __len__(self):
        return len(self._value_storage)
