import re
from argparse import ArgumentParser
from asyncio import Queue, create_task, run
from collections import Counter
from pprint import PrettyPrinter

from aiohttp import ClientSession
from aiohttp.web import HTTPException
from bs4 import BeautifulSoup


def print_response(response):
    printer = PrettyPrinter()
    printer.pprint(response)


class Fetcher:
    def __init__(self, workers_count=10, words_count=3, max_size=10):
        self._words_count = words_count
        self._workers_count = workers_count

        self._workers = []
        self._session = None

        self._queue = Queue(max_size)

    def parse_url(self, page):
        bsoup = BeautifulSoup(page, features="html.parser")
        words = re.findall(r"\w+", bsoup.get_text().lower())
        most_common = dict(Counter(words).most_common(self._words_count))
        return most_common

    async def _fetch_url(self, session, callback):
        while True:
            url = await self._queue.get()

            try:
                async with session.get(url) as resp:
                    page = await resp.text()
                    callback(self.parse_url(page))
            except HTTPException as err:
                print(err)
            except Exception as err:
                print(err)
            finally:
                self._queue.task_done()

    def start(self, callback):
        self._session = ClientSession()
        self._workers = [
            create_task(self._fetch_url(self._session, callback))
            for _ in range(self._workers_count)
        ]

    async def fetch(self, urls):
        for url in urls:
            await self._queue.put(url)

    async def stop(self):
        await self._queue.join()
        await self._session.close()
        for worker in self._workers:
            worker.cancel()


async def main():
    parser = ArgumentParser()
    parser.add_argument("-c", default=10, help="Workers count", type=int)
    parser.add_argument("-f", default="data/urls.txt",
                        help="File path")
    parser.add_argument("-m", default=10, help="Max queue size", type=int)
    parser.add_argument("-w", default=3, help="Words count", type=int)

    fetcher_args = parser.parse_args()
    fetcher = Fetcher(fetcher_args.c, fetcher_args.w, fetcher_args.m)

    fetcher.start(print_response)
    with open(fetcher_args.f, "r", encoding="utf-8") as urls_file:
        for url in urls_file:
            await fetcher.fetch([url])

    await fetcher.stop()


if __name__ == "__main__":
    run(main())
