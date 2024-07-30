import json
import os

default_config = {"notify": True, "skip_weekends": False, "hour": 9, "minute": 30}


def save_config(config, filename="settings/config.json"):
    with open(filename, "w+") as file:
        json.dump(config, file, indent=4)


def load_config_file(filename="settings/config.json"):
    with open(filename, "r") as file:
        return json.load(file)


def load_config(filename="settings/config.json"):
    if os.path.exists(filename):
        return load_config_file(filename)
    else:
        return default_config

CONFIG = load_config()