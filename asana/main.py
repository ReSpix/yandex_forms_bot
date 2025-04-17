import asyncio
import logging
import sys
from typing import NoReturn
from asana_wrapper import publish_asana_task
from nats_wrapper import NATSWrapper
from nats.aio.msg import Msg


async def message_handler(msg: Msg):
    logging.info(f"Получено сообщение: {msg.data.decode()}")
    publish_asana_task(msg.data.decode())
    await msg.ack()


async def main() -> None:
    nats = NATSWrapper()
    await nats.subscribe(message_handler, 'asana-listener')
    await asyncio.Future()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout, format='[%(levelname)s] %(message)s')
    logging.info("Asana startup")
    asyncio.run(main())
