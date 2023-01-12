import sys
from paraphrase import Paraphrase
from lyrics import Lyrics, setup_config, get_text


class WrongOptionTypeError(Exception):
    def __init__(self):
        super().__init__("Input is not an available option")


class Interface:
    def __init__(self, config):
        self.option = None
        self.text = None
        self.paraphrase = None
        self.changed_text = None
        self.config = setup_config(config)

    def get_option(self, limit):
        try:
            option = input("Wybierz opcję: ")
            option = str(option)
            option = option.strip(" ()-.")
            if int(option) not in range(1, limit+1):
                raise ValueError
            self.option = option
        except ValueError:
            raise WrongOptionTypeError

    def choose_option(self):
        print(self)
        self.get_option(5)
        option = self.option
        if option == "1":
            self.help()
        elif option == "2":
            self.generate_random_text()
        elif option == "3":
            self.upload_text_from_file()
        elif option == "4":
            self.choose_paraphrase()
        elif option == "5":
            self.end_program()
        else:
            raise WrongOptionTypeError

    def __str__(self):
        description = """
        1. Help
        2. Generate random text
        3. Upload text from file
        4. Paraphrase the text
        5. Quit\n """
        return description

    def help(self):
        output = self.config["help"]
        print(output)
        _ = input(" ")

    def generate_random_text(self):
        print("""
        1. Generate random song
        2. Generate random poem
        3. Back to menu\n""")
        self.get_option(3)
        option = self.option
        if option == "1":
            self.generate_random_song()
        elif option == "2":
            self.generate_random_poem()
        else:
            self.choose_option()

    def generate_random_song(self):
        pass

    def generate_random_poem(self):
        self.text = Lyrics(get_text(self.config["urls"], "random_poem"))
        print("\n")
        print(self.text)

    def upload_text_from_file():
        pass

    def choose_paraphrase(self):
        print("""
        1. Switch rhymes
        2. Use synonyms
        3. Add adjectives
        4. Back to menu\n""")
        self.get_option(4)
        option = self.option
        if option == "1":
            self.create_paraphrase("rhyme")
        elif option == "2":
            self.create_paraphrase("synonym")
        elif option == "3":
            self.create_paraphrase("adjective")
        else:
            self.choose_option()

    def choose_accuracy(self):
        print("""
        1. High accuracy - low variety
        2. Medium accuracy - medium variety
        3. Low accuracy - high variety
        4. Back to paraphrases\n""")
        self.get_option(4)
        option = self.option
        if option == "1":
            return 1
        elif option == "2":
            return 4
        elif option == "3":
            return 10
        else:
            self.choose_paraphrase()

    def choose_words_to_modify(self):
        print("""
        1. Modify last word in a verse.
        2. Modify first word in a verse.
        3. Modify random word in a verse.
        4. Modify every word in every verse(VERY slow).""")
        self.get_option(5)
        option = self.option
        if option == "1":
            return "last"
        elif option == "2":
            return "first"
        elif option == "3":
            return "random"
        elif option == "4":
            return "all"
        else:
            self.choose_paraphrase()

    def create_paraphrase(self, type):
        change = self.choose_words_to_modify()
        accuracy = self.choose_accuracy()
        self.paraphrase = Paraphrase(self.config["urls"], self.text,
                                     type, change, accuracy)
        self.changed_text = self.paraphrase.create_lyrics()
        print("\n")
        print(self.changed_text)

    def end_program():
        sys.exit()
