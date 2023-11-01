# pylint: disable=protected-access

from dataclasses import dataclass
import unittest
import unittest.mock

from itertools import count
from urllib.error import HTTPError, URLError
from http.client import HTTPMessage
from io import StringIO
from server import NetProtocol, Server, parse_url
from client import Client


class TestNetwork(unittest.TestCase):
    def test_make_msg(self):
        net = NetProtocol()
        data = "https://ru.wikipedia.org/wiki/Python"

        msg = net.make_msg(data, False)
        self.assertEqual(
            msg, "0https://ru.wikipedia.org/wiki/Python\n".encode()
        )

        msg = net.make_msg(data, True)
        self.assertEqual(
            msg, "1https://ru.wikipedia.org/wiki/Python\n".encode()
        )

        msg = net.make_msg("abc")
        self.assertEqual(msg, "0abc\n".encode())

        msg = net.make_msg("")
        self.assertEqual(msg, "0\n".encode())

    def test_read_msg(self):
        net = NetProtocol()

        msg = "0https://ru.wikipedia.org/wiki/Python\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(
            data, [(False, "https://ru.wikipedia.org/wiki/Python")]
        )

        msg = "1https://ru.wikipedia.org/wiki/Python\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(
            data, [(True, "https://ru.wikipedia.org/wiki/Python")]
        )

        msg = "0\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "")])

        msg = "0abc\n1qwerty\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "abc"), (True, "qwerty")])

        msg = "0abc\n1qwerty\n0inbuff".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "abc"), (True, "qwerty")])
        self.assertEqual(net.buffer, "0inbuff")

        msg = "abc\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "inbuffabc")])


class TestClinet(unittest.TestCase):
    @unittest.mock.patch("socket.socket")
    def test_parse_file(self, _):
        client = Client(queue_size=3)
        with open("tests_data/case1.txt", "r", encoding="utf-8") as urls:
            client._parse_file(urls)

        urls_list = []
        while not client._urls_pool.empty():
            urls_list.append(client._urls_pool.get(timeout=1))
        self.assertListEqual(
            urls_list, [("address1", True), ("address2", True), ("address3", False)]
        )

    @unittest.mock.patch("socket.socket")
    def test_parse_empty_file(self, _):
        client = Client()
        with open("tests_data/empty_file.txt", "r", encoding="utf-8") as urls:
            client._parse_file(urls)

        self.assertTrue(client._urls_pool.empty())

    @unittest.mock.patch("socket.socket")
    def test_make_request(self, socket_mock):
        client = Client(queue_size=4)
        with open("tests_data/case1.txt", "r", encoding="utf-8") as urls:
            client._parse_file(urls)
        client._urls_pool.put((None, None))

        net = NetProtocol()

        socket_inst = socket_mock.return_value
        socket_inst.sendall.return_value = None
        socket_inst.recv.return_value = net.make_msg("response")

        with unittest.mock.patch("builtins.print") as print_mock:
            client._make_request()

            self.assertEqual(socket_inst.sendall.call_count, 3)
            self.assertEqual(socket_inst.recv.call_count, 3)
            self.assertEqual(
                [unittest.mock.call("response")] * 3, print_mock.mock_calls
            )


class TestServer(unittest.TestCase):
    @unittest.mock.patch("server.BeautifulSoup")
    def test_parse_url(self, bs_mock):
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

        bs_instance = bs_mock.return_value
        for case in test_cases:
            bs_instance.get_text.return_value = case["text"]

            with unittest.mock.patch("server.urlopen"):
                result = parse_url("", 4)

            self.assertEqual(case["expected_result"], result)

    @unittest.mock.patch("socket.socket")
    def test_worker_routine(self, socket_mock):
        server = Server()
        net = NetProtocol()

        test_tasks = [
            (True, "data", socket_mock),
            (True, "data", socket_mock),
            (False, "data", socket_mock),
            None,
        ]
        for task in test_tasks:
            server._task_queue.put(task)
        server._task_queue.task_done()

        socket_inst = socket_mock.return_value
        socket_inst.sendall.return_value = None
        socket_inst.close.return_value = None

        response = {"response": "something"}
        test_func = unittest.mock.Mock(return_value=response)
        expected_result = str(response).replace("'", '"')
        expected_result = f"data: {expected_result}"
        expected_result = net.make_msg(expected_result)

        with unittest.mock.patch("builtins.print"):
            server._worker_routine(test_func)

        self.assertEqual(test_func.call_count, 3)
        self.assertEqual(socket_mock.sendall.call_count, 3)
        self.assertEqual(socket_mock.close.call_count, 1)
        self.assertEqual(3, next(server._tasks_processed))

        self.assertEqual(
            [unittest.mock.call(expected_result)] * 3,
            socket_mock.sendall.mock_calls,
        )

    @unittest.mock.patch("socket.socket")
    def test_worker_routine_with_exceptions(self, socket_mock):
        server = Server()
        net = NetProtocol()

        test_tasks = [
            (True, "value", socket_mock),
            (True, "http", socket_mock),
            (False, "url", socket_mock),
            None,
        ]
        for task in test_tasks:
            server._task_queue.put(task)
        server._task_queue.task_done()

        socket_inst = socket_mock.return_value
        socket_inst.sendall.return_value = None
        socket_inst.close.return_value = None

        fake_fd = StringIO()

        def raise_exception(exception):
            if exception == "value":
                raise ValueError("error")
            if exception == "http":
                raise HTTPError(
                    "error", 400, HTTPMessage(""), HTTPMessage(""), fake_fd
                )
            if exception == "url":
                raise URLError("error")

        expected_result = [
            net.make_msg("value: error"),
            net.make_msg("http: HTTP error: 400"),
            net.make_msg("url: network error"),
        ]

        with unittest.mock.patch("builtins.print"):
            server._worker_routine(raise_exception)

        self.assertEqual(socket_mock.sendall.call_count, 3)
        self.assertEqual(3, next(server._tasks_processed))
        self.assertEqual(
            [unittest.mock.call(res) for res in expected_result],
            socket_mock.sendall.mock_calls,
        )

        self.assertEqual(socket_mock.close.call_count, 1)

    @unittest.mock.patch("socket.socket")
    def test_start(self, socket_mock):
        server = Server(queue_size=3)
        net = NetProtocol()

        test_req = [
            net.make_msg("request1", keep_alive=True),
            net.make_msg("request2", keep_alive=True),
            None,
            net.make_msg("request3", keep_alive=True),
        ]

        @dataclass
        class FakeConnection:
            def __init__(self, requests):
                self.requests = requests
                self.counter = count()

            def recv(self, _):
                i = next(self.counter)
                if i < len(self.requests):
                    return self.requests[i]
                raise KeyboardInterrupt

        socket_inst = socket_mock.return_value
        socket_inst.accept.return_value = FakeConnection(test_req), None

        with unittest.mock.patch("builtins.print"):
            server.start(None, workers_count=0)

        self.assertTrue(server._task_queue.full())
        for req in test_req:
            if req is None:
                continue
            expected = net.read_msg(req)
            result = server._task_queue.get(timeout=1)[:2]
            self.assertEqual(*expected, result)
