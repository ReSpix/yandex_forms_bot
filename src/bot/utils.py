from datetime import datetime
import requests
from urllib.parse import quote
from .settings import CONFIG
from core import on_new_response

messages_text = [
    "Взято в работу",
    "Позвонили клиенту",
    "Клиент принял работу",
    "Клиент отказался",
]


def get_new_text(current_text, add_text):
    txt = current_text.split("\n")

    if txt[-1] in messages_text:
        txt[-1] = add_text
    else:
        txt.append("")
        txt.append(add_text)

    return "\n".join(txt)


def get_original_text(current_text):
    txt = current_text.split("\n")

    if txt[-1] in messages_text:
        return "\n".join(txt[:-2])

    return current_text


def save_response(text, username, type):
    text = get_original_text(text)
    # text = quote(text)
    on_new_response(text, username, type)
    # url = f"http://api:8000/response/{text}/{username}/{type}"
    # res = requests.get(url)
    # return res.text


def is_notify_skip():
    global_skip = not CONFIG['notify']
    weekend_skip = CONFIG["skip_weekends"] and is_weekend(datetime.now())
    
    if global_skip:
        return True
    elif weekend_skip:
        return True
    
    return False


def is_weekend(date):
    day_of_week = date.weekday()
    return day_of_week == 5 or day_of_week == 6
