"""
Задание 1
Тесты для функции
"""
import unittest
from unittest import mock

from json_filter_func import parse_json


class ParseJsonTestCase(unittest.TestCase):
    """Тесты для функции"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword_callback = mock.Mock(return_value="new_value")

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_parse_json_valid(self):
        """Тест для валидных данных"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        result = parse_json(
            json_str, required_fields, keywords, self.keyword_callback
        )
        self.assertEqual(
            result, '{"key1": "Word1 new_value", "key2": "word2 word3"}'
        )
        self.keyword_callback.assert_called_once_with("word2")

    def test_parse_json_empty(self):
        """Тест для пустых значений"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = []
        keywords = ["word2"]
        result = parse_json(
            json_str, required_fields, keywords, self.keyword_callback
        )
        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = []
        result = parse_json(
            json_str, required_fields, keywords, self.keyword_callback
        )
        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )

    def test_parse_json_none_values(self):
        """Тест для не переданных значений"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        result = parse_json(json_str, keywords, self.keyword_callback)
        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )

        result = parse_json(json_str, required_fields, self.keyword_callback)
        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )

        result = parse_json(json_str, required_fields, keywords)
        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )

    def test_parse_json_missing_required_fields(self):
        """Тест для отсутствующего ключа"""
        json_str = '{"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        result = parse_json(
            json_str, required_fields, keywords, self.keyword_callback
        )

        self.assertEqual(result, '{"key2": "word2 word3"}')

        self.keyword_callback.assert_not_called()

    def test_parse_json_missing_keywords(self):
        """Тест для отсутствующего значения"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word4"]

        result = parse_json(
            json_str, required_fields, keywords, self.keyword_callback
        )

        self.assertEqual(
            result, '{"key1": "Word1 word2", "key2": "word2 word3"}'
        )
        self.keyword_callback.assert_not_called()

    def test_parse_json_invalid_json(self):
        """Тест для неверной json строки"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"'
        required_fields = ["key1"]
        keywords = ["word2"]

        with self.assertRaises(ValueError):
            parse_json(
                json_str, required_fields, keywords, self.keyword_callback
            )

        self.keyword_callback.assert_not_called()

    def test_parse_json_invalid_arguments(self):
        """Тест для неверного типа данных"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = "key1"
        keywords = ["word2"]
        with self.assertRaises(TypeError):
            parse_json(
                json_str, required_fields, keywords, self.keyword_callback
            )
        self.keyword_callback.assert_not_called()

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = "word2"
        with self.assertRaises(TypeError):
            parse_json(
                json_str, required_fields, keywords, self.keyword_callback
            )
        self.keyword_callback.assert_not_called()

        json_str = 1
        required_fields = ["key1"]
        keywords = ["word2"]
        with self.assertRaises(TypeError):
            parse_json(
                json_str, required_fields, keywords, self.keyword_callback
            )
        self.keyword_callback.assert_not_called()

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        with self.assertRaises(TypeError):
            parse_json(json_str, required_fields, keywords, 1)
        self.keyword_callback.assert_not_called()
