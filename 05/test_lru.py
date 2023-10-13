"""
Задание 1
Тесты для LRU Cache
"""

import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    """Класс с тестами"""

    def test_set(self):
        """Тест для установки значений"""
        cache = LRUCache(3)

        for i in range(3):
            cache.set(f"k{i}", f"v{i}")

        self.assertEqual(str(cache), str({"k0": "v0", "k1": "v1", "k2": "v2"}))

        cache.set("k3", "v3")
        self.assertEqual(str(cache), str({"k1": "v1", "k2": "v2", "k3": "v3"}))

        cache["k4"] = "v4"
        self.assertEqual(str(cache), str({"k2": "v2", "k3": "v3", "k4": "v4"}))

    def test_get(self):
        """Тест для получения значений"""
        cache = LRUCache(3)

        for i in range(3):
            cache.set(f"k{i}", f"v{i}")

        self.assertEqual(cache.get("k0"), "v0")

        cache.set("k3", "v3")
        self.assertEqual(str(cache), str({"k1": "v1", "k2": "v2", "k3": "v3"}))
        self.assertIsNone(cache["k0"])
        self.assertEqual(cache["k3"], "v3")

    def test_change_limit(self):
        """Тест для изменения размера кэша"""
        cache = LRUCache(10)

        for i in range(10):
            cache.set(f"k{i}", f"v{i}")

        cache.change_limit(3)
        self.assertEqual(str(cache), str({"k7": "v7", "k8": "v8", "k9": "v9"}))

        cache.change_limit(4)
        cache["k0"] = "v0"
        self.assertEqual(
            str(cache),
            str({"k7": "v7", "k8": "v8", "k9": "v9", "k0": "v0"}),
        )

    def test_simple(self):
        """Тест для проверки значений и размера"""
        cache = LRUCache(3)

        for i in range(3):
            cache.set(f"k{i}", f"v{i}")
        for i in range(3):
            self.assertEqual(cache.get(f"k{i}"), f"v{i}")

        self.assertEqual(cache.size, 3)

    def test_get_not_exist_key(self):
        """Тест для несуществующего значения"""
        cache = LRUCache()
        self.assertIsNone(cache.get("key"))
        self.assertEqual(str(cache), "{}")

    def test_removal(self):
        """Тест для установки большего кол-ва значений чем размер кэша"""
        cache = LRUCache(3)

        for i in range(5):
            cache.set(f"k{i}", f"v{i}")
        for i in range(2, 5):
            self.assertEqual(cache.get(f"k{i}"), f"v{i}")

        self.assertEqual(cache.get("k2"), "v2")
        cache.set("key", "value")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("key"), "value")
        self.assertEqual(
            str(cache), str({"k3": "v3", "k4": "v4", "key": "value"})
        )

        self.assertEqual(cache.size, 3)

    def test_set_exist_key(self):
        """Тест для переопределения значения"""
        cache = LRUCache(2)

        cache.set("k0", "v0")
        cache.set("k1", "v1")
        self.assertEqual(str(cache), str({"k0": "v0", "k1": "v1"}))
        cache.set("k0", "val")
        self.assertEqual(str(cache), str({"k1": "v1", "k0": "val"}))
        cache.set("k2", "v2")

        self.assertEqual(str(cache), str({"k0": "val", "k2": "v2"}))
        self.assertIsNone(cache.get("k1"))

        for _ in range(3):
            cache.set("k0", "v0")

        self.assertEqual(str(cache), str({"k2": "v2", "k0": "v0"}))

        self.assertEqual(cache.size, 2)
        self.assertEqual(cache.get("k0"), "v0")
        self.assertEqual(str(cache), str({"k2": "v2", "k0": "v0"}))
        self.assertEqual(cache.get("k2"), "v2")
        self.assertEqual(str(cache), str({"k0": "v0", "k2": "v2"}))

    def test_small_size(self):
        """Тест для кэша единичного размера"""
        cache = LRUCache(1)

        cache.set("k0", "v0")
        self.assertEqual(cache.get("k0"), "v0")

        cache.set("k1", "v1")
        self.assertIsNone(cache.get("k0"))
        self.assertEqual(cache.get("k1"), "v1")
        self.assertEqual(str(cache), str({"k1": "v1"}))

    def test_incorrect_limit(self):
        """Тест для некорректного размера кэша"""
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-1)
