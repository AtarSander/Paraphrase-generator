import requests
import json
import random


with open("urls.json", "r") as file:
    URL = json.load(file)


def get_text(type, phrase=None, variety=5):
    url = URL[type]
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


class Paraphrase:
    def __init__(self, lyrics):
        self._lyrics = lyrics.lines()

    def count_syllabs(self):
        pass

    def correct_upper(self, word, new_word):
        if word.isupper():
            return new_word.upper()
        if word[0].isupper():
            return new_word.capitalize()
        return new_word

    def correct_punctuation(self, word, new_word):
        marks = """.,!?:;'-")"""
        if word[-1] in marks:
            return new_word + word[-1]
        if word[0] in "(":
            return "(" + new_word
        return new_word

    def choose_words(self, word, option, variety):
        results = []
        data = get_text(option, word.strip("., !?';"), variety)
        for words in data:
            if len(word) >= 4:
                results.append(words["word"])
        return results

    def switch_words(self, line, option, variety):
        new_line = []
        for word in line.split():
            data = self.choose_words(word, option, variety)
            if data:
                new_word = random.choice(data)
                new_word = self.correct_upper(word, new_word)
                new_line.append(self.correct_punctuation(word, new_word))
            else:
                new_line.append(word)
        return " ".join(new_line)

    def create_lyrics(self, option, variety=5):
        new_lyrics = []
        for line in self._lyrics:
            new_lyrics.append(self.switch_words(line, option, variety))
        return "\n".join(new_lyrics)

