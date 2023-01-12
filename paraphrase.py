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

    def highlight_text(self, word):
        return colored(word, "green")

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

    def randomize_word(self, word):
        data = self.choose_words(word)
        if data:
            new_word = random.choice(data)
            new_word = self.correct_upper(word, new_word)
            new_word = self.highlight_text(new_word)
            new_word = self.correct_punctuation(word, new_word)
            return new_word
        else:
            return word

    def create_lyrics(self):
        new_lyrics = []
        for line in self._lyrics:
            if self.option == "adjective":
                new_lyrics.append(self.add_adjectives(line))
            else:
                new_lyrics.append(self.switch_words(line))
        return "\n".join(new_lyrics)

    def add_adjectives(self, line):
        new_line = []
        for word in line.split():
            data = self.choose_words(word)
            if data:
                adjective = random.choice(data)
                adjective = self.correct_upper(word, adjective)
                adjective = self.highlight_text(adjective)
                new_line.append(adjective)
                new_line.append(word)
            else:
                new_line.append(word)
        return " ".join(new_line)
