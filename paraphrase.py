import random
from lyrics import get_text


class Paraphrase:
    def __init__(self, lyrics):
        self._lyrics = lyrics.lines()

    def count_syllabs(self, data):
        return data["numSyllables"]

    def correct_upper(self, word, new_word):
        if word.isupper():
            return new_word.upper()
        if word[0].isupper() or word[1].isupper():
            return new_word.capitalize()
        return new_word

    def correct_punctuation(self, word, new_word):
        marks = """.,!?:;'-")"""
        if word[-1] in marks:
            new_word += word[-1]
        if word[0] in "(\"":
            new_word = word[0] + new_word
        return new_word

    def choose_words(self, word, option, variety):
        results = []
        data = get_text(option, word.strip(".,\" !?';:()-"), variety)
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
            if option == "adjective":
                new_lyrics.append(self.add_adjectives(line, variety))
            else:
                new_lyrics.append(self.switch_words(line, option, variety))
        return "\n".join(new_lyrics)

    def add_adjectives(self, line, variety):
        new_line = []
        for word in line.split():
            data = self.choose_words(word, "adjective", variety)
            if data:
                adjective = random.choice(data)
                adjective = self.correct_upper(word, adjective)
                new_line.append(adjective)
                new_line.append(word)
            else:
                new_line.append(word)
        return " ".join(new_line)
