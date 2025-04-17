import asyncio
from functools import wraps
from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext
from nats.js.api import StreamConfig
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

    @staticmethod
    def retry(failure_text : str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                retries_amount = 5
                current_retry = 1
                while current_retry <= retries_amount:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        logging.info(failure_text + f" {current_retry}/{retries_amount}")
                        if current_retry == retries_amount:
                            raise
                        current_retry += 1
                        await asyncio.sleep(1)
            return wrapper
        return decorator
            
    @retry("Ошибка подключения к NATS")
    async def connect(self):
        "Подключение к NATS JetStream"
        await self.nc.connect(servers=[self.nats_url])
        self.js = self.nc.jetstream()
        logging.info("Подключение к NATS успешно")

        await self._initialize_stream(self.stream_name, self.subject_name)

    async def _get_js(self):
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
        except Exception:
            logging.info(f"Поток {self.stream_name} не найден. Создаю.")
            js = await self._get_js()
            await js.add_stream(
                config=StreamConfig(name=name, subjects=[subject])
            )
            logging.info(f"Поток {self.stream_name} создан.")

    async def close(self):
        "Закрытие соединения с NATS"
        await self.nc.drain()

    async def publish(self, text: str):
        "Публикация текста в поток jetstream"
        js = await self._get_js()
        return await js.publish(self.subject_name, text.encode())

    @retry(f"Неудачное подключение к потоку")
    async def subscribe(self, callback_func: Callable, durable_name: str):
        "Push подписка на поток"
        js = await self._get_js()

        await js.subscribe(self.subject_name, durable_name, cb=callback_func, stream=self.stream_name)
