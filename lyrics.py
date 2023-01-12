import requests
import json


def setup_config(source, option=None):
    with open(source, "r") as file:
        config = json.load(file)
    if option:
        return config[option]
    else:
        return config


def get_text(url, type, phrase=None, variety=5):
    url = url[type]
    text = requests.get(url.format(word=phrase, number=variety)).json()
    return text


class Lyrics:
    def __init__(self, text):
        self._title = text[0]["title"]
        self._author = text[0]["author"]
        self._lines = text[0]["lines"]

    def author(self):
        return self._author

    def title(self):
        return self._title

    def lines(self):
        return self._lines

    def __str__(self):
        text = "\n".join(self._lines)
        return text
