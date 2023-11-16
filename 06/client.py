"""Клиент"""

import socket

from queue import Queue
from argparse import ArgumentParser
from threading import Thread
from server import NetProtocol


class Client:
    """Класс клиента"""
    def __init__(self, address="localhost", port=8080, queue_size=10):
        self.address = address
        self.port = port

        # Создание экземпляра класса NetProtocol
        self._net = NetProtocol()

        # Создание пустого списка для потоков
        self._thread_list = []

        # Создание очереди с максимальным размером queue_size
        self._urls_pool = Queue(queue_size)

        # Создание клиентского сокета
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, fileobj, threads_count=1):
        """Метод start используется для установления соединения с сервером, запуска потоков и обработки файла."""
        # Подключение к серверу
        self._socket.connect((self.address, self.port))

        # Создаем потоки
        self._start_threads(threads_count)

        # Парсим файл
        self._parse_file(fileobj)

        # Закрытие соединения с сервером
        self.stop()

    def stop(self):
        """Метод stop используется для остановки работы клиента, ожидания завершения потоков и закрытия сокета."""
        for thread in self._thread_list:
            # Ожидание завершения всех потоков
            thread.join()

        # Закрытие сокета
        self._socket.close()

    def _start_threads(self, threads_count):
        """Метод _start_threads создает заданное количество потоков для выполнения запросов к серверу."""
        # Создание списка потоков с количеством threads_count
        self._thread_list = [
            Thread(target=self._make_request) for _ in range(threads_count)
        ]
        # Запуск каждого потока
        for thread in self._thread_list:
            thread.start()

    def _parse_file(self, fileobj):
        """Метод _parse_file используется для чтения URL-адресов из файла, добавления их в очередь и передачи потокам для обработки."""
        urls = []
        for line in fileobj:
            if line.strip() == "":
                continue
            # Добавление очищенной строки в список urls
            urls.append(line.strip())

        for i, url in enumerate(urls):
            # Добавление URL в очередь с флагом keep_alive=False
            if i == len(urls) - 1:
                self._urls_pool.put((url, False))
            # Добавление URL в очередь с флагом keep_alive=True
            else:
                self._urls_pool.put((url, True))

        # Добавление None в очередь для каждого потока
        for _ in enumerate(self._thread_list):
            self._urls_pool.put((None, None))

    def _make_request(self):
        """Метод _make_request выполняет отправку запросов к серверу и получение ответов, после чего выводит сообщения."""
        while True:
            # Получение URL и флага keep_alive из очереди
            url, keep_alive = self._urls_pool.get()
            # Если получен None, выход из цикла
            if url is None:
                break

            # Создание сообщения с помощью метода make_msg из экземпляра класса NetProtocol
            msg = self._net.make_msg(url, keep_alive)
            # Отправка сообщения по сокету
            self._socket.sendall(msg)
            # Получение ответа от сервера
            resp = self._socket.recv(1024)
            # Чтение сообщений из ответа с помощью метода read_msg из экземпляра класса NetProtocol
            messages = self._net.read_msg(resp)

            for msg in messages:
                print(msg[1])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f",  default='urls.txt', help="File with urls")
    parser.add_argument("-t", default=1, help="Therads count")

    args = parser.parse_args()

    client = Client()

    with open(args.f, "r", encoding="utf-8") as urls_file:
        client.start(urls_file, threads_count=int(args.t))

    client.stop()
