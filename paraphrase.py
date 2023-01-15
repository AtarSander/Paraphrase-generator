import random
from lyrics import get_text
from termcolor import colored


class Paraphrase:
    """
    This is the class for generating a paraphrase of given text.

    :param url: dictionary with urls to be used for different options
    :type url: dict

    :param lyrics: lyrics to be paraphrased
    :type lyrics: Lyrics

    :param option: type of paraphrase ('rhyme', 'synonym', 'adjective')
    :type option: str

    :param change: word in text to be changed('all', 'first', 'last', 'random')
    :type change: str

    :param variety: how many options of modified words to choose from
    :type variety: int

    :param changed_lyrics: the final version of the text
    :type changed_lyrics: str
    """
    def __init__(self, url, lyrics, option="synonym",
                 change="first", variety=5):
        self.url = url
        self._lyrics = lyrics.lines()
        self.option = option
        self.change = change
        self.variety = variety
        self.changed_lyrics = None

    @staticmethod
    def highlight_text(word):
        """
        Returns the word in green color.
        """
        return colored(word, "green")

    @staticmethod
    def correct_upper(word, new_word):
        """
        Corrects capitalization of new_word.

        Checks if the word is in uppercase then returns new_word in uppercase,
        if only first or second sign is uppercase returns new_word capitalized.
        """
        if word.isupper():
            return new_word.upper()
        if word[0].isupper() or word[1].isupper():
            return new_word.capitalize()
        return new_word

    @staticmethod
    def correct_punctuation(word, new_word):
        """
        Corrects punctuation of new_word.

        Checks if the first or last character of the word is punctuation mark
        then adds the same to new_word.
        """
        marks = """.,!?:;'-")"""
        if word[-1] in marks:
            new_word += word[-1]
        if word[0] in '("':
            new_word = word[0] + new_word
        return new_word

    def choose_words(self, word):
        """
        Returns list of synonyms, rhymes or adjectives(option) for given word.

        If word is longer than 4 letters fetches using get_text function and
        returns synonyms, rhymes or adjectives (according to option) of
        results. Max length of results according to variety.
        """
        results = []
        if len(word) >= 4:
            data = get_text(self.url, self.option,
                            word.strip(".,\" !?';:()-"), self.variety)
            for words in data:
                results.append(words["word"])
        return results

    def randomize_word(self, word, is_adjective=False):
        """
        Chooses random word and corrects it given the data from choose_words().

        Chooses random new_word from data given by choose_words method, if
        adjective is false corrects it and return new_word else returns
        new_word without correction. If data is empty, returns None if
        adjective is false else returns word.
        """
        data = self.choose_words(word)
        if data:
            new_word = random.choice(data)
            if not is_adjective:
                new_word = self.correct_upper(word, new_word)
                new_word = self.highlight_text(new_word)
                new_word = self.correct_punctuation(word, new_word)
            return new_word
        else:
            if not is_adjective:
                return word
            else:
                return None

    def switch_words(self, line):
        """
        Returns newline with switched word according to change for given line

        Chooses which word in line to switch according to change param,
        switches it for a new one given by randomize_word method.
        """
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

    def insert_adjective(self, line, index, all=False):
        """
        Inserts adjective into a line given the index.

        Checks if new_word given by randomize_word method is not empty,
        if true corrects new_word. Then if all is false new_word
        is inserted into line in index position and the line is returned.
        If all is true new_word, word tuple is returned.
        """
        word = line[index]
        new_word = self.randomize_word(word, True)
        # rewrite
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
        """
        Returns newline with added adjective according to change for given line

        Chooses to which word add the adjective according to change param, then
        inserts it using insert_adjective method.
        """
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
        """
        Returns final paraphrase changed_lyrics given every line in _lyrics.
        """
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
        self.changed_lyrics = "\n".join(new_lyrics)
        return self.changed_lyrics
