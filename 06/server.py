"""Сервер"""

import re
import json
import socket
import urllib.error

from argparse import ArgumentParser
from collections import Counter
from itertools import count
from queue import Queue
from threading import Thread, current_thread
from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup


def parse_url(url, words_count):
    """Функция поиска наиболее часто встречающихся слов на странице"""
    with urlopen(url, timeout=2) as page:
        # Создаем объект BeautifulSoup для парсинга страницы
        bsoup = BeautifulSoup(page.read(), features="html.parser")

    # Находим все слова на странице
    words = re.findall(r"\w+", bsoup.get_text().lower())
    # Находим наиболее часто встречающиеся слова
    most_common = dict(Counter(words).most_common(words_count))
    return most_common


class NetProtocol:
    def __init__(self):
        self.buffer = ""

    def make_msg(self, data, keep_alive=False):
        """Метод формирования сообщения"""
        keep_alive = int(keep_alive)
        result = f"{keep_alive}{data}\n"
        return result.encode()

    def read_msg(self, data):
        """Метод чтения сообщения"""
        data = data.decode()

        # Разделение сообщений
        messages = f"{self.buffer}{data}".split("\n")
        # Проверка последнего сообщения
        if messages[-1] != "":
            # Сохранение оставшейся части сообщения
            self.buffer = messages[-1]
        # Удаление пустого элемента
        del messages[-1]

        for i, msg in enumerate(messages):
            messages[i] = (bool(int(msg[0])), msg[1:])

        return messages


class Server:
    def __init__(self, address="localhost", port=8080, queue_size=10):
        self.address = address
        self.port = port

        self._net = NetProtocol()

        self._tasks_processed = count()

        self._thread_list = []
        self._task_queue = Queue(queue_size)
        # Создание сокета
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Установка параметров сокета
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, func, *args, workers_count=1, backlog=0):
        """Метод запуска сервера"""
        print("Strarting server with args:", f"{func=}, {args=}, {backlog=}")
        # Привязка сокета к адресу и порту
        self._socket.bind((self.address, self.port))
        # Начало прослушивания сокета
        self._socket.listen(backlog)
        # Запуск воркеров
        self._start_workers(workers_count, func, *args)

        while True:
            try:
                # Принятие входящего соединения
                conn, _ = self._socket.accept()
                # Очистка буфера
                self._net.buffer = ""
                # Установка флага keep_alive в True
                keep_alive = True
                while keep_alive:
                    # Получение данных из соединения
                    req = conn.recv(1024)
                    # Проверка наличия данных
                    if not req:
                        break
                    # Чтение сообщений
                    messages = self._net.read_msg(req)
                    # Получение значения keep_alive
                    keep_alive = messages[-1][0]

                    for msg in messages:
                        # Добавление сообщений в очередь задач
                        self._task_queue.put((*msg, conn))
            except KeyboardInterrupt:
                self.stop()
                break

    def stop(self):
        """Метод остановки сервера"""
        for _ in enumerate(self._thread_list):
            # Добавление элементов None в очередь задач
            self._task_queue.put(None)
        for thread in self._thread_list:
            # Ожидание завершения потока
            thread.join()
        # Закрытие сокета
        self._socket.close()

    def _start_workers(self, workers_count, func, *args):
        """М    етод для запуска воркеров"""
        print("Strarting", workers_count, "workers")
        self._thread_list = [
            # Создание потока для выполнения задачи
            Thread(target=self._worker_routine, args=(func, *args))
            for _ in range(workers_count)
        ]
        for thread in self._thread_list:
            # Запуск потока
            thread.start()

    def _worker_routine(self, func, *args):
        """Метод для выполнения задачи воркера"""
        # Вывод сообщения о начале выполнения задачи воркера
        print("Strart routine at thread:", current_thread())
        while True:
            # Получение задачи из очереди
            task = self._task_queue.get()
            # Проверка наличия задачи
            if task is None:
                break
            # Получение данных из задачи
            keep_alive, data, conn = task
            resp = ''
            try:
                resp = func(data, *args)
                # Преобразование результата в JSON-строку
                resp = json.dumps(resp, ensure_ascii=False)
                # Формирование ответа
                resp = f"{data}: {resp}"
            except ValueError as err:
                resp = f"{data}: {err}"
            except urllib.error.HTTPError as err:
                resp = f"{data}: HTTP error: {err.code}"
            except urllib.error.URLError:
                resp = f"{data}: network error"
            finally:
                # Отправка ответа по соединению conn
                conn.sendall(self._net.make_msg(resp))
                # Отметка выполненной задачи
                self._task_queue.task_done()

            print(
                "Number of processed tasks:",
                next(self._tasks_processed) + 1,
            )

            if keep_alive is False:
                while self._task_queue.unfinished_tasks > 0:
                    sleep(0.5)
                conn.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-w", default=1, help="Workers count")
    parser.add_argument("-k", default=5, help="Number of most common words")

    server_args = parser.parse_args()

    server = Server()
    server.start(
        parse_url, int(server_args.k), workers_count=int(server_args.w)
    )
