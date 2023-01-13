import random
from lyrics import get_text
from termcolor import colored


class Paraphrase:
    def __init__(self, url, lyrics, option="synonym",
                 change="first", variety=5):
        self.url = url
        self._lyrics = lyrics.lines()
        self.option = option
        self.change = change
        self.variety = variety

    @staticmethod
    def highlight_text(word):
        return colored(word, "green")

    @staticmethod
    def correct_upper(word, new_word):
        if word.isupper():
            return new_word.upper()
        if word[0].isupper() or word[1].isupper():
            return new_word.capitalize()
        return new_word

    @staticmethod
    def correct_punctuation(word, new_word):
        marks = """.,!?:;'-")"""
        if word[-1] in marks:
            new_word += word[-1]
        if word[0] in '("':
            new_word = word[0] + new_word
        return new_word

    def choose_words(self, word):
        results = []
        data = get_text(self.url, self.option,
                        word.strip(".,\" !?';:()-"), self.variety)
        for words in data:
            if len(word) >= 4:
                results.append(words["word"])
        return results

    def switch_words(self, line):
        new_line = []
        if self.change == "all":
            for word in line.split():
                new_line.append(self.randomize_word(word))
        elif self.change == "first":
            new_line = line.split()
            if new_line:
                new_line[0] = self.randomize_word(new_line[0])
        elif self.change == "last":
            new_line = line.split()
            if new_line:
                new_line[-1] = self.randomize_word(new_line[-1])
        else:
            new_line = line.split()
            picked = random.choice(new_line)
            index = new_line.index(picked)
            new_line[index] = self.randomize_word(new_line[index])
        return " ".join(new_line)

    def randomize_word(self, word, adjective=False):
        data = self.choose_words(word)
        if data:
            new_word = random.choice(data)
            if not adjective:
                new_word = self.correct_upper(word, new_word)
                new_word = self.highlight_text(new_word)
                new_word = self.correct_punctuation(word, new_word)
            return new_word
        else:
            if not adjective:
                return word
            else:
                return None

    def insert_adjective(self, line, index, all=False):
        word = line[index]
        new_word = self.randomize_word(word, True)
        if new_word:
            if index == 0:
                new_word = self.correct_upper("Capital letter", new_word)
                word = word.lower()
                line[0] = word
            new_word = self.highlight_text(new_word)
            if all:
                return new_word, word
            line.insert(index, new_word)
        if not all:
            return line
        else:
            return word

    def add_adjectives(self, line):
        words = line.split()
        new_line = words
        if self.change == "all":
            new_line = []
            for index, _ in enumerate(words):
                adjective_tuple = self.insert_adjective(words, index, True)
                if type(adjective_tuple) == tuple:
                    new_line.append(adjective_tuple[0])
                    new_line.append(adjective_tuple[1])
                else:
                    new_line.append(adjective_tuple)
        elif self.change == "first":
            new_line = self.insert_adjective(new_line, 0)
        elif self.change == "last":
            new_line = self.insert_adjective(new_line, -1)
        else:
            picked = random.choice(words)
            index = new_line.index(picked)
            new_line = self.insert_adjective(new_line, index)
        return " ".join(new_line)

    def create_lyrics(self):
        new_lyrics = []
        if self.option == "adjective":
            for line in self._lyrics:
                if line:
                    new_lyrics.append(self.add_adjectives(line))
                else:
                    new_lyrics.append(line)
        else:
            for line in self._lyrics:
                if line:
                    new_lyrics.append(self.switch_words(line))
                else:
                    new_lyrics.append(line)
        return "\n".join(new_lyrics)
