"""
Задание 1
Тесты для функции
"""
import unittest
from unittest.mock import patch
from json_filter_func import parse_json


class TestParseJson(unittest.TestCase):
    """Unittest класс с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_correct_work(self):
        """Проверка валидных данных"""
        with patch("json_filter_func.change_word") as mock_fetch:
            mock_fetch.return_value = "измененное слово"
            # Проверки с валидными условиями
            self.assertEqual(
                '{"key1": "Word1 измененное слово", "key2": "word2 word3"}',
                parse_json(
                    '{"key1": "Word1 word2", "key2": "word2 word3"}',
                    ["key1"],
                    ["wOrD2"],
                    keyword_callback=mock_fetch,
                ),
            )
            self.assertEqual(
                '{"key1": "Word1 измененное слово измененное слово", '
                '"key2": "word2 word3"}',
                parse_json(
                    '{"key1": "Word1 word2 word4", "key2": "word2 word3"}',
                    ["key1"],
                    ["wOrD2", "word4"],
                    keyword_callback=mock_fetch,
                ),
            )
            self.assertEqual(
                '{"key1": "Word1 измененное слово измененное слово", '
                '"key2": "измененное слово word3"}',
                parse_json(
                    '{"key1": "Word1 word2 word4", "key2": "word2 word3"}',
                    ["key1", "key2"],
                    ["wOrD2", "word4"],
                    keyword_callback=mock_fetch,
                ),
            )
            # Проверка с дефолтными аргументами
            self.assertEqual(
                '{"key1": "Word1 word2", "key2": "word2 word3"}',
                parse_json('{"key1": "Word1 word2", "key2": "word2 word3"}'),
            )
            # Проверка с отсутствующим ключом в json-строке
            self.assertEqual(
                '{"key1": "Word1 word2", "key2": "word2 word3"}',
                parse_json(
                    '{"key1": "Word1 word2", "key2": "word2 word3"}',
                    ["key3"],
                    ["wOrD2", "word4"],
                    keyword_callback=mock_fetch,
                ),
            )
            # Проверка с пустым списком ключей
            self.assertEqual(
                '{"key1": "Word1 word2", "key2": "word2 word3"}',
                parse_json(
                    '{"key1": "Word1 word2", "key2": "word2 word3"}',
                    [],
                    ["wOrD2", "word4"],
                    keyword_callback=mock_fetch,
                ),
            )
            self.assertEqual(len(mock_fetch.mock_calls), 6)

    def test_invalid_incorrect_data_type(self):
        """Проверка ошибки TypeError"""
        with patch("json_filter_func.change_word") as mock_fetch:
            mock_fetch.return_value = "измененное слово"
            # Проверка с неверным типом json_str
            self.assertRaises(
                TypeError, parse_json, 1, keyword_callback=mock_fetch
            )
            # Проверка с неверным типом required_fields
            self.assertRaises(
                TypeError, parse_json, "", 1, [""], keyword_callback=mock_fetch
            )
            # Проверка с неверным типом keywords
            self.assertRaises(
                TypeError,
                parse_json,
                "",
                required_fields=["test"],
                keywords=1,
                keyword_callback=mock_fetch,
            )
            # Проверка с неверным типом keyword_callback
            self.assertRaises(
                TypeError,
                parse_json,
                "",
                required_fields=["test"],
                keywords=["test"],
                keyword_callback=1,
            )
            # Проверка с неверным типом элемента required_fields
            self.assertRaises(
                TypeError,
                parse_json,
                "",
                required_fields=[1],
                keywords=["test"],
                keyword_callback=mock_fetch,
            )
            # Проверка с неверным типом элемента keywords
            self.assertRaises(
                TypeError,
                parse_json,
                "",
                required_fields=["test"],
                keywords=[1],
                keyword_callback=mock_fetch,
            )
            self.assertEqual(len(mock_fetch.mock_calls), 0)

    def test_invalid_incorrect_data(self):
        """Проверка ошибки ValueError"""
        with patch("json_filter_func.change_word") as mock_fetch:
            mock_fetch.return_value = "измененное слово"
            # Проверки с неверным значением json_str
            self.assertRaises(
                ValueError,
                parse_json,
                "",
                ["test"],
                ["test"],
                keyword_callback=mock_fetch,
            )
            self.assertRaises(
                ValueError,
                parse_json,
                "52",
                ["test"],
                ["test"],
                keyword_callback=mock_fetch,
            )
            self.assertEqual(len(mock_fetch.mock_calls), 0)
