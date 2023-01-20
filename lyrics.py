import requests
import json


def setup_config(source, option=None):
    """
    Opens json file and loads it into a variable

    :param source: path to json file
    :type source: str

    :param option: (optional) key to return specific value from json file
    :type option: str

    :return: json object or specific value from json object
    """
    with open(source, "r") as file:
        config = json.load(file)
    if option:
        return config[option]
    else:
        return config


def get_text(url, form, phrase=None, variety=5):
    """
    Fetch data from specified url

    :param url: base url
    :type option: str

    :param form: endpoint for specific content
    :type option: str

    :param phrase: (optional) word to include in url
    :type option: str

    :param variety: (optional) number of results to return
    :type option: int

    :return: json object
    """
    url = url[form]
    text = requests.get(url.format(word=phrase, number=variety)).json()
    return text


class Lyrics:
    """
    This class stores and formats lyrics with all its contents.

    :param text: file with lyrics to format
    :type option: json object

    :param option: (optional) "Poem" or "Song"
    :type option: str
    """
    def __init__(self, text, option="Poem"):
        if option == "Poem":
            text = self.format_poem(text)
            self._author = text["author"]
            self._lines = text["lines"]
        else:
            self._author = text["artist"]
            self._lines = self.format_song(text)
        self._title = text["title"]

    def author(self):
        """
        Returns author
        """
        return self._author

    def set_author(self, author):
        """
        Sets author
        """
        self._author = author

    def title(self):
        """
        Returns title
        """
        return self._title

    def set_title(self, title):
        """
        Sets title
        """
        self._title = title

    def lines(self):
        """
        Returns lines
        """
        return self._lines

    def set_lines(self, lines):
        """
        Sets lines
        """
        self._lines = lines

    def __str__(self):
        """
        Returns string representation of lyrics
        """
        text = "\n".join(self._lines)
        return text

    def format_poem(self, text):
        """
        Formats text taking into account how poem is fetched from API
        """
        text = text[0]
        return text

    def format_song(self, text):
        """
        Formats text taking into account how song is fetched from API
        """
        text = text["lyrics"].strip("Embed1234567890")
        lines = text.split("\n")
        return lines[1:]
