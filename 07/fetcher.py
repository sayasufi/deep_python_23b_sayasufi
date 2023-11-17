"""
Скрипт для асинхронной обкачки урлов
"""
# pylint: disable=E0401

import asyncio
import os
import re
from asyncio import Queue, create_task
from collections import Counter
from argparse import ArgumentParser
from aiohttp import ClientSession
from aiohttp.web import HTTPException
from bs4 import BeautifulSoup


def arg_parser():
    """Parsing command line arguments and returning the result"""
    parser = ArgumentParser()
    parser.add_argument(
        "c", default=10, help="Workers count", type=int, nargs="?", const=10
    )
    parser.add_argument(
        "f", default="urls.txt", help="File path", nargs="?", const="urls.txt"
    )
    parser.add_argument(
        "-w", default=3, help="Words count", type=int, required=False
    )

    return parser


def print_response(response, url):
    """
    Функция print_response принимает на вход результат
    парсинга страницы и выводит его на экран
    """
    print(f"{url.strip()} {response}")


class Fetcher:
    """
    Класс Fetcher отвечает за загрузку и парсинг веб-страниц
    """

    def __init__(
        self,
        workers_count: int = 10,
        path: str = "urls.txt",
        urls_vn: list[str] | None = None,
        words_count: int = 3,
    ):
        """
        Метод init инициализирует необходимые
        переменные и создает очередь задач
        """
        if workers_count <= 0 or words_count <= 0:
            raise ValueError

        if not isinstance(path, str):
            raise TypeError

        if urls_vn is not None:
            if not isinstance(urls_vn, list):
                raise TypeError
            for i in urls_vn:
                if not isinstance(i, str):
                    raise TypeError

        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, path)
        if not os.path.exists(file_path):
            raise FileNotFoundError

        self._words_count = words_count
        self._path = path
        self.urls_vn = urls_vn
        self._workers_count = workers_count

        self._workers = []
        self._session = None
        self.errors = {}

        self._queue = Queue(10)

    def parse_url(self, page):
        """
        Метод parse_url принимает на вход HTML-код страницы и
        с помощью библиотеки BeautifulSoup извлекает текст и находит
        наиболее часто встречающиеся слова. Результат возвращается в
        виде словаря.
        """
        bsoup = BeautifulSoup(page, features="html.parser")
        words = re.findall(r"\w+", bsoup.get_text().lower())
        most_common = dict(Counter(words).most_common(self._words_count))
        return most_common

    async def _fetch_url(self, session, callback):
        """
        Метод _fetch_url является асинхронной функцией, которая
        выполняется в отдельном потоке. Он извлекает URL-адрес
        из очереди и загружает страницу с помощью библиотеки aiohttp.
        Затем результат парсинга передается в функцию callback.
        """
        while True:
            url = await self._queue.get()
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        page = await resp.text()
                        callback(self.parse_url(page), url)
                    else:
                        self.errors[url.strip()] = resp.status
            except HTTPException as err:
                self.errors[url] = str(f"HTTPException: {err}")
            except Exception as err:
                self.errors[url] = str(f"Exception: {err}")
            finally:
                self._queue.task_done()

    async def start(self, callback):
        """
        Метод start запускает процесс загрузки и парсинга страниц.
        Он создает экземпляр класса ClientSession из библиотеки aiohttp
        и запускает несколько рабочих потоков для обработки задач.
        """
        self._session = ClientSession()
        self._workers = [
            create_task(self._fetch_url(self._session, callback))
            for _ in range(self._workers_count)
        ]

        if self.urls_vn:
            for url in self.urls_vn:
                await self.fetch([url])

        else:
            with open(self._path, "r", encoding="utf-8") as urls_file:
                for url in urls_file:
                    await self.fetch([url])

        await self.stop()

    async def fetch(self, urls):
        """
        Метод fetch добавляет URL-адреса в очередь задач.
        """
        for url in urls:
            await self._queue.put(url)

    async def stop(self):
        """
        Метод stop останавливает процесс загрузки и парсинга страниц.
        Он дожидается завершения всех задач в очереди,
        закрывает сессию и отменяет все рабочие потоки.
        """
        await self._queue.join()
        await self._session.close()
        for worker in self._workers:
            worker.cancel()


if __name__ == "__main__":
    # Функция main является точкой входа в программу.
    # Она парсит аргументы командной строки с помощью ArgumentParser,
    # создает экземпляр класса Fetcher и запускает процесс загрузки и
    # парсинга страниц. URL-адреса читаются из файла urls.txt.

    fetcher_args = arg_parser().parse_args()

    fetcher = Fetcher(
        workers_count=fetcher_args.c,
        path=fetcher_args.f,
        urls_vn=None,
        words_count=fetcher_args.w,
    )
    asyncio.run(fetcher.start(print_response))
