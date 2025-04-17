from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext
from nats.js.api import StreamConfig
import logging


class NATSWrapper:
    "Обертка для работы с NATS"

    def __init__(self):
        self.stream = "messages"
        self.subject = "message.new"
        self.nats_url = "nats://nats:4222"
        self.nc = NATS()
        self.js: JetStreamContext | None = None

    async def connect(self):
        "Подключение к NATS JetStream"
        await self.nc.connect(servers=[self.nats_url])
        self.js = self.nc.jetstream()

        await self._initialize_stream(self.stream, self.subject)

    def _get_js(self):
        "Получение объекта jetstream"
        if self.js is None:
            raise ConnectionError("Подключение к JetStream еще не выполнено")
        return self.js

    async def _initialize_stream(self, name: str, subject: str):
        "Проверка существования нужного потока в jetstream и создание при отсутствии"
        logging.info(f"Проверка потока.")
        try:
            await self._get_js().stream_info(name)
        except Exception:
            logging.info(f"Поток {self.stream} не найдет. Создаю.")
            await self._get_js().add_stream(
                config=StreamConfig(name=name, subjects=[subject])
            )
            logging.info(f"Поток {self.stream} создан.")

    async def close(self):
        "Закрытие соединения с NATS"
        await self.nc.drain()

    async def publish(self, text: str):
        "Публикация текста в поток jetstream"
        return await self._get_js().publish(self.subject, text.encode())


nats_wrapper = NATSWrapper()
