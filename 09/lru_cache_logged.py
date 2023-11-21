"""
Логирование LRUCache
"""
# pylint: disable=W1203
import logging
from argparse import ArgumentParser


class LRUCache:
    """Класс LRUCache"""

    def __init__(self, limit: int = 10):
        if not isinstance(limit, int):
            raise TypeError
        if limit <= 0:
            raise ValueError
        self._value_storage: dict = {}
        self._limit: int = limit
        logging.info(f"Init lru_cache with {limit=}")

    def get(self, key):
        """Функция для получения значений"""
        if key in self._value_storage:
            value = self._value_storage.get(key)
            del self._value_storage[key]
            logging.debug(f"Delete item by {key=}, {value=}")
            self._value_storage[key] = value
            logging.debug(f"Set item by {key=}, {value=}")
            logging.info(f"Get item by {key=}, {value=}")
            logging.debug(f"Current state {self._value_storage}")
            return value
        logging.warning(f"Get item by {key=}, key is missing")
        return None

    def set(self, key, value):
        """Функция для установки значения"""
        if key in self._value_storage:
            del self._value_storage[key]
            logging.info(
                f"Delete item by {key=}, {value=} from cache, "
                f"because a new key will be installed"
            )

        self._insert_item(key, value)
        self._pop_items()

    def change_limit(self, limit: int):
        """Функция для изменения размера кэша"""
        self._limit: int = limit
        logging.info(f"Changed lru_cache limit to {limit}")
        self._pop_items()

    def _pop_items(self):
        """Функция для удаления элементов"""
        while len(self._value_storage) > self._limit:
            key = next(iter(self._value_storage))
            del self._value_storage[key]
            logging.warning(
                f"Delete item by {key=} from cache, "
                f"because the container is full"
            )
            logging.debug(f"Current state {self._value_storage}")

    def _insert_item(self, key, value):
        """Функция для установки значений в словарь"""
        self._value_storage[key] = value
        logging.info(f"Set {key=}, {value=} in cache")
        logging.debug(f"Current state {self._value_storage}")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __str__(self):
        return str(self._value_storage)

    def __len__(self):
        return len(self._value_storage)


def setup_logging(
    log_file, stdout_logging: bool = False, custom_filter: bool = False
):
    """Создаем функцию инициализирующую логгер"""
    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Создаем форматтер для логов
    formatter = logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Если указан аргумент командной строки "-s",
    # добавляем обработчик для вывода в stdout
    if stdout_logging:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.WARNING)
        stdout_handler.setFormatter(
            logging.Formatter("%(levelname)s - %(message)s")
        )
        logger.addHandler(stdout_handler)

    # Если указан аргумент командной строки "-f", добавляем кастомный фильтр
    if custom_filter:

        def custom_filter_chet(record):
            """Кастомный фильтр, отбрасывающий записи с четным числом слов"""
            return len(record.msg.split()) % 2 != 0

        logger.addFilter(custom_filter_chet)

    return logger


def main():
    """Точка входа"""
    parser = ArgumentParser()
    parser.add_argument(
        "-s", action="store_true", help="Enable stdout logging"
    )
    parser.add_argument("-f", action="store_true", help="Enable custom filter")
    args = parser.parse_args()

    log_file = "cache.log"
    stdout_logging = args.s
    custom_filter = args.f

    setup_logging(log_file, stdout_logging, custom_filter)

    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


if __name__ == "__main__":
    main()
