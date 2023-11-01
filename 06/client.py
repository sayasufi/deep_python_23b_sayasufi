import socket

from queue import Queue
from argparse import ArgumentParser
from threading import Thread
from server import NetProtocol


class Client:
    def __init__(self, address="localhost", port=8080, queue_size=10):
        self.address = address
        self.port = port

        self._net = NetProtocol()

        self._thread_list = []

        self._urls_pool = Queue(queue_size)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, fileobj, threads_count=1):
        self._socket.connect((self.address, self.port))
        self._start_threads(threads_count)

        self._parse_file(fileobj)
        self.stop()

    def stop(self):
        for thread in self._thread_list:
            thread.join()
        self._socket.close()

    def _start_threads(self, threads_count):
        self._thread_list = [
            Thread(target=self._make_request) for _ in range(threads_count)
        ]
        for thread in self._thread_list:
            thread.start()

    def _parse_file(self, fileobj):
        urls = []
        for line in fileobj:
            if line.strip() == "":
                continue

            urls.append(line.strip())

        for i, url in enumerate(urls):
            if i == len(urls) - 1:
                self._urls_pool.put((url, False))
            else:
                self._urls_pool.put((url, True))

        for _ in enumerate(self._thread_list):
            self._urls_pool.put((None, None))

    def _make_request(self):
        while True:
            url, keep_alive = self._urls_pool.get()
            if url is None:
                break

            msg = self._net.make_msg(url, keep_alive)
            self._socket.sendall(msg)
            resp = self._socket.recv(1024)
            messages = self._net.read_msg(resp)

            for msg in messages:
                print(msg[1])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help="File with urls")
    parser.add_argument("-t", default=1, help="Therads count")

    args = parser.parse_args()

    client = Client()

    with open(args.f, "r", encoding="utf-8") as urls_file:
        client.start(urls_file, threads_count=int(args.t))

    client.stop()
