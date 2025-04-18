import asyncio
from functools import wraps
from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext
from nats.js.api import StreamConfig
from nats.js.errors import NotFoundError
from nats.js.api import DeliverPolicy
import logging
from typing import Callable


class NATSWrapper:
    "Обертка для работы с NATS"

    def __init__(self):
        self.stream_name = "messages"
        self.subject_name = "message.new"
        self.nats_url = "nats://nats:4222"
        self.nc = NATS()
        self.js: JetStreamContext | None = None
        self.nats_errors: list[Exception] = []

    @staticmethod
    def retry(failure_text: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                retries_amount = 5
                current_retry = 1
                while current_retry <= retries_amount:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        logging.info(failure_text +
                                     f" {current_retry}/{retries_amount}")
                        if current_retry == retries_amount:
                            raise
                        current_retry += 1
                        await asyncio.sleep(1)
            return wrapper
        return decorator

    async def _disconnected(self):
        logging.info("Потеряно соединение с NATS")

    async def _reconnected(self):
        logging.info("Подключение к NATS восстановлено")
        for e in self.nats_errors:
            logging.info("Ошибки NATS при последнем разрыве:")
            logging.info(f"{type(e)}:{e}")
        self.nats_errors.clear()

    async def _on_error(self, e: Exception):
        self.nats_errors.append(e)

    @retry("Ошибка подключения к NATS")
    async def connect(self):
        "Подключение к NATS JetStream"
        self.nats_errors.clear()
        await self.nc.connect(servers=[self.nats_url],
                              disconnected_cb=self._disconnected,
                              reconnected_cb=self._reconnected,
                              error_cb=self._on_error,
                              max_reconnect_attempts=-1)
        self.js = self.nc.jetstream()
        logging.info("Подключение к NATS успешно")

        await self._initialize_stream(self.stream_name, self.subject_name)

    async def _get_js(self) -> JetStreamContext:
        "Получение объекта jetstream"
        if self.js is None:
            logging.info("Нет подключения к JetStream. Подключаюсь...")
            await self.connect()
            if self.js is None:
                raise Exception("Не удалось подключиться к NATS JetStream")

        return self.js

    async def _initialize_stream(self, name: str, subject: str):
        "Проверка существования нужного потока в jetstream и создание при отсутствии"
        logging.info(f"Проверка потока.")
        try:
            js = await self._get_js()
            await js.stream_info(name)
            logging.info(f"Поток {self.stream_name} найден.")
        except NotFoundError:
            logging.info(f"Поток {self.stream_name} не найден. Создаю.")
            js = await self._get_js()
            await js.add_stream(
                config=StreamConfig(name=name,
                                    subjects=[subject],
                                    max_bytes=100 * 1024 * 1024,  # ограничение на 100 Мб
                                    )
            )
            logging.info(f"Поток {self.stream_name} создан.")

    async def close(self):
        "Закрытие соединения с NATS"
        try:
            await self.nc.drain()
        except Exception as e:
            logging.warning(
                "Не удалось мягко закрыть соединение с NATS. Отключаюсь жестко")
            await self.nc.close()

    async def publish(self, text: str):
        "Публикация текста в поток jetstream"
        js = await self._get_js()
        return await js.publish(self.subject_name, text.encode())

    @retry(f"Неудачное подключение к потоку")
    async def subscribe(self, callback_func: Callable, durable_name: str):
        "Push подписка на поток"
        js = await self._get_js()

        await js.subscribe(self.subject_name,
                           durable_name,
                           cb=callback_func,
                           stream=self.stream_name,
                           manual_ack=True,
                           deliver_policy=DeliverPolicy.NEW)
