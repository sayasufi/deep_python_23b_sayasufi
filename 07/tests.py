""""
Тесты для скрипта асинхронной обкачки урлов
"""

# pylint: disable=protected-access
# pylint: disable=E0401

from asyncio import create_task

from unittest.mock import AsyncMock, Mock, call, patch, MagicMock
from asynctest import IsolatedAsyncioTestCase

from faker import Faker
from fetcher import Fetcher, print_response, HTTPException, arg_parser


class TestFetcher(IsolatedAsyncioTestCase):
    """
    Тест кейс для асинхронной обкачки урлов
    """

    def test_parse_url(self):
        """
        Функция test_parse_url тестирует метод parse_url класса Fetcher
        """
        test_cases = [
            {
                "text": "word, ..'word'', qwerty %(QWERTY something!@ +)WORD&(@%",  # noqa
                "expected_result": {"word": 3, "qwerty": 2, "something": 1},
            },
            {"text": "", "expected_result": {}},
            {
                "text": "word qwerty something",
                "expected_result": {"word": 1, "qwerty": 1, "something": 1},
            },
        ]
        # Используется патч для замены объекта BeautifulSoup
        # на мок-объект, чтобы можно было проверить вызовы
        # методов этого объекта
        with patch("fetcher.BeautifulSoup") as bs_mock:
            bs_instance = bs_mock.return_value
            for case in test_cases:
                bs_instance.get_text.return_value = case["text"]

                fetcher = Fetcher(1, "")
                result = fetcher.parse_url("")

                self.assertEqual(case["expected_result"], result)

    async def test_fetch_url(self):
        """
        Функция test_fetch_url тестирует метод _fetch_url класса Fetcher.
        """
        fake = Faker()
        # Создается несколько случайных URL-адресов и текст страницы.
        urls = [fake.url() for _ in range(5)]
        page_text = fake.text()

        # Создается экземпляр Fetcher и для каждого
        # URL-адреса добавляется в очередь.
        fetcher = Fetcher()
        for url in urls:
            await fetcher._queue.put(url)

        # Создается мок-объект session_mock, который будет
        # использоваться для выполнения запросов
        session_mock = Mock()
        # Устанавливается возвращаемое значение метода get мок-объекта
        # session_mock, чтобы возвращался мок-объект resp_mock, у
        # которого установлено возвращаемое значение метода text
        resp_mock = AsyncMock()
        session_mock.get.return_value = resp_mock
        resp_mock.__aenter__.return_value.text.return_value = page_text
        resp_mock.__aenter__.return_value.status = 200
        # Создается мок-объект callback_mock,
        # который будет вызываться после получения текста страницы
        callback_mock = Mock()

        # Запускается асинхронная задача _fetch_url, ожидается,
        # пока очередь не будет пустой, и затем задача отменяется
        task = create_task(fetcher._fetch_url(session_mock, callback_mock))
        await fetcher._queue.join()
        task.cancel()

        # Проверяется, что очередь пуста, вызывался правильное
        # количество раз метод callback_mock и что вызовы метода
        # callback_mock были сделаны с правильными аргументами.
        self.assertTrue(fetcher._queue.empty())

        expected_result = fetcher.parse_url(page_text)
        self.assertEqual(callback_mock.call_count, len(urls))
        self.assertEqual(
            callback_mock.mock_calls,
            [call(expected_result, urls[i]) for i in range(5)],
        )

    async def test_start(self):
        """
        Функция test_start тестирует метод start класса Fetcher
        """
        # Создается экземпляр Fetcher с количеством рабочих потоков 5 и
        # вызывается метод start с мок-объектом в качестве аргумента
        fetcher = Fetcher(workers_count=5, urls_vn=[""])
        await fetcher.start(Mock())
        # Проверяется, что для каждого рабочего потока не
        # вызывался метод done, то есть они все еще выполняются.
        for worker in fetcher._workers:
            self.assertFalse(worker.done())

        await fetcher.stop()

    @patch("builtins.open")
    async def test_start_without_urls_vn(self, mock_open):
        """Тест для start с файлом"""
        urls_file = MagicMock()
        urls_file.__enter__.return_value = urls_file
        urls_file.__iter__.return_value = ["url1"]
        mock_open.return_value = urls_file

        obj = Fetcher()
        obj._path = "urls.txt"

        await obj.start(Mock())

        mock_open.assert_called_once_with("urls.txt", "r", encoding="utf-8")

    @patch("builtins.open")
    async def test_start_empty_urls_vn(self, mock_open):
        """Тест для start с пустым файлом"""
        urls_file = MagicMock()
        urls_file.__enter__.return_value = urls_file
        urls_file.__iter__.return_value = ["url1"]
        mock_open.return_value = urls_file

        obj = Fetcher()
        obj.urls_vn = []

        await obj.start(Mock())

        mock_open.assert_called_once_with(obj._path, "r", encoding="utf-8")

    async def test_fetch(self):
        """
        Функция test_fetch тестирует метод fetch класса Fetcher
        """
        fake = Faker()
        urls = [fake.url() for _ in range(10)]

        # Создается несколько случайных URL-адресов, создается
        # экземпляр Fetcher с количеством рабочих потоков 5 и
        # максимальным размером очереди 10
        fetcher = Fetcher(workers_count=5)
        await fetcher.fetch(urls)

        # Для каждого URL-адреса добавляется в очередь и затем проверяется,
        # что он извлекается из очереди и помечается как выполненный
        for url in urls:
            self.assertEqual(await fetcher._queue.get(), url)
            fetcher._queue.task_done()

    async def test_print_response(self):
        """Тесты для функции print_response"""
        response = "Response"
        url = "http://example.com"
        expected_output = "http://example.com Response"

        with patch("builtins.print") as mock_print:
            print_response(response, url)
            mock_print.assert_called_once_with(expected_output)

    async def test_exception(self):
        """Тесты для ошибок Exception"""

        def fake_exception(*args):
            """Функция вызывающая Exception"""
            raise Exception("404")

        urls = ["https://example"]
        fetcher = Fetcher()
        for url in urls:
            await fetcher._queue.put(url)

        session_mock = Mock()

        resp_mock = AsyncMock()
        session_mock.get.return_value = resp_mock
        resp_mock.__aenter__.return_value.text.return_value = "page_text"
        resp_mock.__aenter__.return_value.status = 200

        task = create_task(fetcher._fetch_url(session_mock, fake_exception))
        await fetcher._queue.join()
        task.cancel()

        expected = {"https://example": "Exception: 404"}
        self.assertEqual(fetcher.errors, expected)

    async def test_fake_http_exception(self):
        """Тесты для ошибки HTTPException"""

        def fake_http_exception(*args):
            """Функция вызывающая HTTPException"""
            raise HTTPException()

        urls = ["https://example"]
        fetcher = Fetcher()
        for url in urls:
            await fetcher._queue.put(url)

        session_mock = Mock()

        resp_mock = AsyncMock()
        session_mock.get.return_value = resp_mock
        resp_mock.__aenter__.return_value.text.return_value = "page_text"
        resp_mock.__aenter__.return_value.status = 200

        task = create_task(
            fetcher._fetch_url(session_mock, fake_http_exception)
        )
        await fetcher._queue.join()
        task.cancel()

        expected = {"https://example": "HTTPException: "}
        self.assertEqual(fetcher.errors, expected)

    async def test_fetch_url_with_404(self):
        """Функция тестирующая ответ сервера не 200"""
        fake = Faker()
        # Создается несколько случайных URL-адресов и текст страницы.
        urls = [fake.url() for _ in range(5)]
        page_text = fake.text()

        # Создается экземпляр Fetcher и для каждого
        # URL-адреса добавляется в очередь.
        fetcher = Fetcher(urls_vn=urls)
        for url in urls:
            await fetcher._queue.put(url)

        session_mock = Mock()

        resp_mock = AsyncMock()
        session_mock.get.return_value = resp_mock
        resp_mock.__aenter__.return_value.text.return_value = page_text
        resp_mock.__aenter__.return_value.status = 404

        callback_mock = Mock()

        task = create_task(fetcher._fetch_url(session_mock, callback_mock))
        await fetcher._queue.join()
        task.cancel()

        expected = dict.fromkeys(urls, 404)
        self.assertTrue(fetcher._queue.empty())
        self.assertEqual(callback_mock.call_count, 0)
        self.assertEqual(callback_mock.mock_calls, [])
        self.assertEqual(fetcher.errors, expected)

    def test_arg_parser(self):
        """Функция тестирующая arg_parser"""
        args = arg_parser().parse_args(["5", "custom.txt", "-w", "5"])
        self.assertEqual(args.c, 5)
        self.assertEqual(args.f, "custom.txt")
        self.assertEqual(args.w, 5)

        args = arg_parser().parse_args([])
        self.assertEqual(args.c, 10)
        self.assertEqual(args.f, "urls.txt")
        self.assertEqual(args.w, 3)

    def test_value_error(self):
        """Тесты для ValueError"""
        with self.assertRaises(ValueError):
            Fetcher(workers_count=-1)
        with self.assertRaises(ValueError):
            Fetcher(words_count=0)

    def test_type_error(self):
        """Тесты для TypeError"""
        with self.assertRaises(TypeError):
            Fetcher(path=1)
        with self.assertRaises(TypeError):
            Fetcher(urls_vn="ffff")
        with self.assertRaises(TypeError):
            Fetcher(urls_vn=[1, 1])

    def test_file_not_found_error(self):
        """Тесты для FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            Fetcher(path="error.txt")
