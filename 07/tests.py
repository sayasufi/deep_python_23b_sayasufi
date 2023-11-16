""""Тесты для скрипта асинхронной обкачки урлов"""
# pylint: disable=protected-access

from asyncio import create_task
from unittest.mock import AsyncMock, Mock, call, patch
from unittest.async_case import IsolatedAsyncioTestCase

from faker import Faker
from fetcher import Fetcher


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

                fetcher = Fetcher(1, 4)
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
        fetcher = Fetcher(workers_count=5)
        fetcher.start(Mock())

        # Проверяется, что для каждого рабочего потока не
        # вызывался метод done, то есть они все еще выполняются.
        for worker in fetcher._workers:
            self.assertFalse(worker.done())

        await fetcher.stop()

    async def test_fetch(self):
        """
        Функция test_fetch тестирует метод fetch класса Fetcher
        """
        fake = Faker()
        urls = [fake.url() for _ in range(10)]

        # Создается несколько случайных URL-адресов, создается
        # экземпляр Fetcher с количеством рабочих потоков 5 и
        # максимальным размером очереди 11
        fetcher = Fetcher(workers_count=5, max_size=11)
        await fetcher.fetch(urls)

        # Для каждого URL-адреса добавляется в очередь и затем проверяется,
        # что он извлекается из очереди и помечается как выполненный
        for url in urls:
            self.assertEqual(await fetcher._queue.get(), url)
            fetcher._queue.task_done()
