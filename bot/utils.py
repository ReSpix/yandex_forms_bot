import requests
from urllib.parse import quote

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
    text = quote(text)
    url = f"http://api:8000/response/{text}/{username}/{type}"
    res = requests.get(url)
    return res.text
