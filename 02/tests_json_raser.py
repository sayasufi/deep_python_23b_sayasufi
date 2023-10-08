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
        self.keyword_callback = mock.Mock()

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_parse_json_valid(self):
        """Тест для валидных данных"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        parse_json(json_str, required_fields, keywords, self.keyword_callback)
        self.keyword_callback.assert_called_once()
        self.keyword_callback.assert_called_with("key1", "word2")

    def test_parse_json_some_values(self):
        """Несколько найденных required_field и keyword"""
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        required_fields = ["key1", "key2"]
        keywords = ["word2", "word1", "WORD4"]
        parse_json(json_str, required_fields, keywords, self.keyword_callback)

        self.keyword_callback.assert_has_calls(
            [
                mock.call("key1", "word2"),
                mock.call("key1", "word1"),
                mock.call("key2", "WORD4"),
            ]
        )
        self.assertEqual(self.keyword_callback.call_count, 3)

    def test_parse_json_match_of_several_keywords(self):
        """Совпадение нескольких keyword в одной строке"""
        json_str = (
            '{"key1": "Word1 word2 word3word1 word1 WORD1",'
            ' "key2": "word3 word4"}'
        )
        required_fields = ["key1"]
        keywords = ["word1"]
        parse_json(json_str, required_fields, keywords, self.keyword_callback)

        self.keyword_callback.assert_called_once()
        self.keyword_callback.assert_called_with("key1", "word1")

    def test_parse_json_valid_word_in_string(self):
        """Тест на полное совпадение"""
        json_str = '{"key1": "Word1word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        parse_json(json_str, required_fields, keywords, self.keyword_callback)
        self.keyword_callback.assert_not_called()

    def test_parse_json_empty(self):
        """Тест для пустых значений"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = []
        keywords = ["word2"]
        parse_json(json_str, required_fields, keywords, self.keyword_callback)
        self.keyword_callback.assert_not_called()

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = []
        parse_json(json_str, required_fields, keywords, self.keyword_callback)
        self.keyword_callback.assert_not_called()

    def test_parse_json_none_values(self):
        """Тест для не переданных значений"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        parse_json(json_str, keywords, self.keyword_callback)
        self.keyword_callback.assert_not_called()

        parse_json(json_str, required_fields, self.keyword_callback)
        self.keyword_callback.assert_not_called()

        parse_json(json_str, required_fields, keywords)
        self.keyword_callback.assert_not_called()

    def test_parse_json_missing_required_fields(self):
        """Тест для отсутствующего ключа"""
        json_str = '{"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        parse_json(json_str, required_fields, keywords, self.keyword_callback)

        self.keyword_callback.assert_not_called()

    def test_parse_json_missing_keywords(self):
        """Тест для отсутствующего значения"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word4"]

        parse_json(json_str, required_fields, keywords, self.keyword_callback)

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
