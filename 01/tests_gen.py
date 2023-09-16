import unittest
from unittest.mock import mock_open, patch
from generator_for_file import gen_search_words


class TestSearchWordsInFile(unittest.TestCase):

    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    # Тест 1
    # Проверка валидных данных, список слов в нижнем регистре
    @patch('builtins.open', new_callable=mock_open, read_data='а Роза упала на лапу Азора\nраз два три\nРозовый цветок')
    def test_search_words(self, mock_open):
        file_name = 'example.txt'
        words = ['роза', 'два']
        result = list(gen_search_words(file_name, words))
        expected_result = ['а Роза упала на лапу Азора', 'раз два три']
        self.assertEqual(result, expected_result)

    # Тест 2
    # Проверка валидных данных, список слов в верхнем регистре
    @patch('builtins.open', new_callable=mock_open, read_data='а Роза упала на лапу Азора\nраз два три\nРозовый цветок')
    def test_search_words_case_insensitive(self, mock_open):
        file_name = 'example.txt'
        words = ['РОЗА', 'ДВА']
        result = list(gen_search_words(file_name, words))
        expected_result = ['а Роза упала на лапу Азора', 'раз два три']
        self.assertEqual(result, expected_result)

    # Тест 3
    # Проверка валидных данных, результат выполнения пустой
    @patch('builtins.open', new_callable=mock_open, read_data='а Роза упала на лапу Азора\nраз два три\nРозовый цветок')
    def test_search_words_no_match(self, mock_open):
        file_name = 'example.txt'
        words = ['четыре', 'пять']
        result = list(gen_search_words(file_name, words))
        expected_result = []
        self.assertEqual(result, expected_result)

    # Тест 4
    # Проверка валидных данных, список слов пустой
    @patch('builtins.open', new_callable=mock_open, read_data='а Роза упала на лапу Азора\nраз два три\nРозовый цветок')
    def test_search_words_no_words(self, mock_open):
        file_name = 'example.txt'
        words = []
        result = list(gen_search_words(file_name, words))
        expected_result = []
        self.assertEqual(result, expected_result)

    # Тест 5
    # Проверка ошибки FileNotFoundError, если файл отсутсвует в директории
    def test_search_words_in_file_with_invalid_file(self):
        file_name = 'example1.txt'
        words = ['роза']
        with self.assertRaises(FileNotFoundError):
            for _ in gen_search_words(file_name, words):
                pass

    # Тест 6
    # Проверка ошибки TypeError, список слов принимает не список, а другой тип данных
    def test_search_words_in_file_with_invalid_type_words(self):
        file_name = 'example.txt'
        words = 123
        with self.assertRaises(TypeError):
            for _ in gen_search_words(file_name, words):
                pass

    # Тест 7
    # Проверка ошибки TypeError, имя файла принимает не string и не является файловым объектом
    def test_search_words_in_file_with_invalid_type_file_object(self):
        file_name = 838
        words = ['роза']
        with self.assertRaises(TypeError):
            for _ in gen_search_words(file_name, words):
                pass

    # Тест 8
    # Проверка ошибки TypeError, список слов принимает не список string, а список других типов данных
    def test_search_words_in_file_with_invalid_type_file_name(self):
        file_name = 'example.txt'
        words = [1, 2, 3]
        with self.assertRaises(TypeError):
            for _ in gen_search_words(file_name, words):
                pass


if __name__ == '__main__':
    unittest.main()
