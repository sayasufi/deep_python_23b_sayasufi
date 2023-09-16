"""
Задание 2
Тестирование функции генератора для чтения и фильтрации файла
"""
import os
import unittest
from unittest.mock import mock_open, patch
from generator_for_file import gen_search_words


class TestSearchWordsInFile(unittest.TestCase):
    """unittest класс с тестами"""

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    # Тест 1
    @patch('builtins.open', new_callable=mock_open,
           read_data='''а Роза упала на лапу Азора
           раз два три
           Розовый цветок'''
           )
    def test_search_words(self, _):
        """Проверка валидных данных, список слов в нижнем регистре"""
        file_name = 'example.txt'
        words = ['роза', 'два']
        result = list(gen_search_words(file_name, words))
        expected_result = ['а Роза упала на лапу Азора', 'раз два три']
        self.assertEqual(result, expected_result)

    # Тест 2
    @patch('builtins.open', new_callable=mock_open,
           read_data='''а Роза упала на лапу Азора
           раз два три
           Розовый цветок'''
           )
    def test_search_words_case_insensitive(self, _):
        """Проверка валидных данных, список слов в верхнем регистре"""
        file_name = 'example.txt'
        words = ['РОЗА', 'ДВА']
        result = list(gen_search_words(file_name, words))
        expected_result = ['а Роза упала на лапу Азора', 'раз два три']
        self.assertEqual(result, expected_result)

    # Тест 3
    @patch('builtins.open', new_callable=mock_open,
           read_data='''а Роза упала на лапу Азора
           раз два три
           Розовый цветок'''
           )
    def test_search_words_no_match(self, _):
        """Проверка валидных данных, результат выполнения пустой"""
        file_name = 'example.txt'
        words = ['четыре', 'пять']
        result = list(gen_search_words(file_name, words))
        expected_result = []
        self.assertEqual(result, expected_result)

    # Тест 4
    @patch('builtins.open', new_callable=mock_open,
           read_data='''а Роза упала на лапу Азора
           раз два три
           Розовый цветок'''
           )
    def test_search_words_no_words(self, _):
        """Проверка валидных данных, список слов пустой"""
        file_name = 'example.txt'
        words = []
        result = list(gen_search_words(file_name, words))
        expected_result = []
        self.assertEqual(result, expected_result)

    # Тест 5
    def test_search_words_in_file_with_invalid_file(self):
        """
        Проверка ошибки FileNotFoundError,
        если файл отсутсвует в директории
        """
        file_name = 'example1.txt'
        words = ['роза']
        with self.assertRaises(FileNotFoundError):
            set(gen_search_words(file_name, words))

    # Тест 6
    def test_search_words_in_file_with_invalid_type_words(self):
        """
        Проверка ошибки TypeError,
        список слов принимает не список, а другой тип данных
        """
        file_name = 'example.txt'
        words = 123
        with self.assertRaises(TypeError):
            set(gen_search_words(file_name, words))

    # Тест 7
    def test_search_words_in_file_with_invalid_type_file_object(self):
        """
        Проверка ошибки TypeError,
        имя файла принимает не string и не является файловым объектом
        """
        file_name = 838
        words = ['роза']
        with self.assertRaises(TypeError):
            set(gen_search_words(file_name, words))

    # Тест 8
    def test_search_words_in_file_with_invalid_type_file_name(self):
        """
        Проверка ошибки TypeError, список слов принимает не список string,
        а список других типов данных
        """
        file_name = 'example.txt'
        words = [1, 2, 3]
        with self.assertRaises(TypeError):
            set(gen_search_words(file_name, words))

    # Тест 9
    def test_search_1(self):
        """
        Проверка валидных данных, если передан открытый файловый объект
        """
        file_name = 'test.txt'
        expected_result = ['а Роза упала на лапу Азора', 'раз два три']
        text = '''а Роза упала на лапу Азора\nраз два три\nРозовый цветок'''
        with open(file_name, 'w', encoding='UTF-8') as file:
            file.write(text)
        file = open('test.txt', 'r', encoding='UTF-8')
        words = ['роза', 'два']
        result = list(gen_search_words(file, words))
        self.assertEqual(result, expected_result)
        file.close()
        os.remove(file_name)
