import os

# TODO: переделать для получения из БД
TOKEN: str = os.getenv("TOKEN") # type: ignore
chat_id: str = os.getenv("CHAT_ID") # type: ignore
api_url = f"https://{ os.getenv("PAGEKITE_URL") }.pagekite.me/api/status"
