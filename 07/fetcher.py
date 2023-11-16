"""
Скрипт для асинхронной обкачки урлов
"""
import asyncio
import re
from argparse import ArgumentParser
from asyncio import Queue, create_task
from collections import Counter

from aiohttp import ClientSession
from aiohttp.web import HTTPException
from bs4 import BeautifulSoup


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

    def __init__(self, workers_count=10, words_count=3, max_size=10):
        """
        Метод init инициализирует необходимые
        переменные и создает очередь задач
        """
        self._words_count = words_count
        self._workers_count = workers_count

        self._workers = []
        self._session = None

        self._queue = Queue(max_size)

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
                    page = await resp.text()
                    callback(self.parse_url(page), url)
            except HTTPException as err:
                print(err)
            except ImportError as err:
                print(err)
            finally:
                self._queue.task_done()

    def start(self, callback):
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


async def main():
    """
    Функция main является точкой входа в программу.
    Она парсит аргументы командной строки с помощью ArgumentParser,
    создает экземпляр класса Fetcher и запускает процесс загрузки и
    парсинга страниц. URL-адреса читаются из файла urls.txt.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "c", default=10, help="Workers count", type=int, nargs="?", const=10
    )
    parser.add_argument(
        "f", default="urls.txt", help="File path", nargs="?", const="urls.txt"
    )
    parser.add_argument(
        "-m", default=10, help="Max queue size", type=int, required=False
    )
    parser.add_argument(
        "-w", default=3, help="Words count", type=int, required=False
    )

    fetcher_args = parser.parse_args()
    fetcher = Fetcher(fetcher_args.c, fetcher_args.w, fetcher_args.m)

    fetcher.start(print_response)
    with open(fetcher_args.f, "r", encoding="utf-8") as urls_file:
        for url in urls_file:
            await fetcher.fetch([url])

    await fetcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
