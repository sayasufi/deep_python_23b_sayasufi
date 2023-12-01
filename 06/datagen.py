"""Генерация файла с заданным кол-вом url"""

import concurrent.futures
from argparse import ArgumentParser
from urllib.request import urlopen


def generate_url(url_scope):
    """Функция, которая открывает случайную
    страницу Википедии и возвращает ее URL"""
    with urlopen(url_scope) as page:
        return page.url


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", default="urls.txt", help="Filename")
    parser.add_argument("-k", default=100, help="URLs count")

    args = parser.parse_args()
    URL = "https://en.wikipedia.org/wiki/Special:Random"

    with open(args.f, "w", encoding="utf-8") as file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Запуск функции generate_url для каждого URL-адреса в пуле потоков
            urls = executor.map(generate_url, [URL] * int(args.k))

            for url in urls:
                file.write(url + "\n")
