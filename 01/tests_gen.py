"""
Задание 2
Тестирование функции генератора для чтения и фильтрации файла
"""
import os
import unittest
from unittest.mock import mock_open, patch

from generator_for_file import gen_search_words


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""а Роза упала на лапу Азора
          раз два три
          Розовый цветок""",
)
class TestSearchWordsInFile(unittest.TestCase):
    """unittest класс с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_open_existing_file(self, _):
        """Валидные тесты"""
        words = ["роза"]
        result = list(gen_search_words("test.txt", words))
        self.assertEqual(result, ["а Роза упала на лапу Азора"])

        words = ["РОЗА", "ДВА"]
        result = list(gen_search_words("test.txt", words))
        self.assertEqual(result, ["а Роза упала на лапу Азора", "раз два три"])

        words = ["роза", "два"]
        result = list(gen_search_words("test.txt", words))
        self.assertEqual(result, ["а Роза упала на лапу Азора", "раз два три"])

        words = ["четыре", "пять"]
        result = list(gen_search_words("test.txt", words))
        self.assertEqual(result, [])

        words = []
        result = list(gen_search_words("test.txt", words))
        self.assertEqual(result, [])

    def test_open_nonexistent_file(self, _):
        """Несуществующий файл"""
        words = ["роза"]
        with self.assertRaises(FileNotFoundError):
            set(gen_search_words("nonexistent.txt", words))
        with self.assertRaises(FileNotFoundError):
            set(gen_search_words("", words))

    def test_open_file_with_empty_name(self, _):
        """Неверный тип данных"""
        words = ["роза"]
        with self.assertRaises(TypeError):
            set(gen_search_words(1, words))

        words = "роза"
        with self.assertRaises(TypeError):
            set(gen_search_words("test.txt", words))

        words = [1, 2]
        with self.assertRaises(TypeError):
            set(gen_search_words("test.txt", words))


class TestSearchWordsInFileWithoutMock(unittest.TestCase):
    """unittest класс 2 с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_searching_strings_from_file_object(self):
        """
        Проверка валидных данных, если передан открытый файловый объект
        """
        file_name = "test1.txt"
        words = ["роза", "два"]
        expected_result = ["а Роза упала на лапу Азора", "раз два три"]
        text = """а Роза упала на лапу Азора\nраз два три\nРозовый цветок"""
        with open(file_name, "w", encoding="UTF-8") as file:
            file.write(text)
        with open("test1.txt", "r", encoding="UTF-8") as file:
            result = list(gen_search_words(file, words))
            self.assertEqual(result, expected_result)
        os.remove(file_name)
