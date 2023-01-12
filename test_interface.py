from interface import Interface, WrongOptionTypeError
from lyrics import Lyrics, setup_config
import pytest
import builtins
import lyrics as ls


test_texts = setup_config("config.json", "test_text")
TEXT1 = test_texts["text1_medium"]


def test_Interface_get_option_correct_input(monkeypatch):
    example_ui = Interface("config.json")

    def mock_input(_):
        return "2"
    monkeypatch.setattr(builtins, "input", mock_input)
    example_ui.get_option(3)
    assert example_ui.option == "2"


def test_Interface_get_option_wrong_input(monkeypatch):
    example_ui = Interface("config.json")

    def mock_input(_):
        return "6"
    monkeypatch.setattr(builtins, "input", mock_input)
    with pytest.raises(WrongOptionTypeError):
        example_ui.get_option(3)


def test_Interface__str__():
    example_ui = Interface("config.json")
    assert str(example_ui) == """
        1. Help
        2. Generate random text
        3. Upload text from file
        4. Paraphrase the text
        5. Quit\n """


def test_Interface_choose_option(monkeypatch):
    example_ui = Interface("config.json")

    def mock_get_option(self, __):
        self.option = "2"
    monkeypatch.setattr(Interface, "get_option", mock_get_option)
    assert example_ui.choose_option() == example_ui.generate_random_text()


def test_Interface_generate_random_text(monkeypatch):
    example_ui = Interface("config.json")

    def mock_get_option(self, __):
        self.option = "2"
    monkeypatch.setattr(Interface, "get_option", mock_get_option)
    assert (
        example_ui.generate_random_text() == example_ui.generate_random_poem()
           )


def test_Interface_generate_random_song(monkeypatch):
    pass


def test_Interface_generate_random_poem(monkeypatch):
    example_ui = Interface("config.json")

    def mock_get_text(_):
        return TEXT1
    monkeypatch.setattr(ls, "get_text", mock_get_text)
    example_ui.generate_random_poem()
    example_ui.text == "\n".join(TEXT1[0]["lines"])


def test_Interface_choose_paraphrase(monkeypatch):
    example_ui = Interface("config.json")
    example_ui.text = Lyrics(TEXT1)

    def mock_get_option(self, __):
        self.option = "1"

    monkeypatch.setattr(Interface, "get_option", mock_get_option)
    assert (
        example_ui.choose_paraphrase() ==
        example_ui.create_paraphrase("synonym")
           )


def test_Interface_choose_paraphrase_back(monkeypatch):
    example_ui = Interface("config.json")
    example_ui.text = Lyrics(TEXT1)

    def mock_get_option(self, __):
        self.option = "3"
    monkeypatch.setattr(Interface, "get_option", mock_get_option)

    def mock_choose_option(_):
        pass
    monkeypatch.setattr(Interface, "choose_option", mock_choose_option)
    assert (
        example_ui.choose_paraphrase() ==
        example_ui.choose_option()
           )


def test_Interface_choose_paraphrase_wrong_input(monkeypatch):
    example_ui = Interface("config.json")
    example_ui.text = Lyrics(TEXT1)

    def mock_get_option(self, __):
        self.option = ["1"]
    monkeypatch.setattr(Interface, "get_option", mock_get_option)
    with pytest.raises(WrongOptionTypeError):
        example_ui.choose_paraphrase()


def test_Interface_choose_accuracy(monkeypatch):
    example_ui = Interface("config.json")
    example_ui.text = Lyrics(TEXT1)

    def mock_get_option(self, __):
        self.option = "3"
    monkeypatch.setattr(Interface, "get_option", mock_get_option)
    assert example_ui.choose_accuracy() == 10
