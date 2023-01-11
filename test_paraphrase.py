from paraphrase import Paraphrase
from lyrics import Lyrics
import random

TEXT2 = [
  {
    "title": "Prayer for Children",
    "author": "William Cowper",
    "lines": [
      "Gracious Lord, our children see,",
      "By Thy mercy we are free;",
      "But shall these, alas! remain",
      "Subjects still of Satan's reign?",
      "Israel's young ones, when of old",
      "Pharaoh threaten'd to withhold,",
      "Then Thy messenger said, \"No;",
      "Let the children also go!\"",
      "",
      "When the angel of the Lord,",
      "Drawing forth his dreadful sword,",
      "Slew with an avenging hand,",
      "All the first-born of the land;",
      "Then Thy people's door he pass'd,",
      "Where the bloody sign was placed:",
      "Hear us, now, upon our knees,",
      "Plead the blood of Christ for these!"
    ],
    "linecount": "16"
  }
]

TEXT3 = [
  {
    "title": "Cancelled Passage of Mont Blanc",
    "author": "Percy Bysshe Shelley",
    "lines": [
      "There is a voice, not understood by all,",
      "Sent from these desert-caves. It is the roar",
      "Of the rent ice-cliff which the sunbeams call,",
      "Plunging into the vale--it is the blast",
      "Descending on the pines--the torrents pour..."
    ],
    "linecount": "5"
  }
]


TEXT4 = [
  {
    "title": "His Heart was darker than the starless night",
    "author": "Emily Dickinson",
    "lines": [
      "His Heart was darker than the starless night",
      "For that there is a morn",
      "But in this black Receptacle",
      "Can be no Bode of Dawn"
    ],
    "linecount": "4"
  }
]


def test_Paraphrase_correct_upper_capitalize():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.correct_upper("Gracious", "good") == "Good"


def test_Paraphrase_correct_upper_all():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.correct_upper("GRACIOUS", "good") == "GOOD"


def test_Paraphrase_correct_punctuation_end():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.correct_punctuation("sword,", "blade") == "blade,"


def test_Paraphrase_correct_punctuation_start():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.correct_punctuation("(sword", "blade") == "(blade"


def test_Paraphrase_correct_punctuation_both():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.correct_punctuation("(sword,", "blade") == "(blade,"


def test_Paraphrase_choose_words_synonyms():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)
    assert generator.choose_words("gracious", "synonym", 6) == ["good",
                                                                "kind",
                                                                "nice",
                                                                "benevolent",
                                                                "elegant",
                                                                "propitious"]


def test_Paraphrase_choose_words_rhymes():
    example_poem = Lyrics(TEXT3)
    generator = Paraphrase(example_poem)
    assert generator.choose_words("pour", "rhyme", 4) == ["for",
                                                          "pore",
                                                          "tor",
                                                          "outpour"]


def test_Paraphrase_switch_words_synonyms(monkeypatch):
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[9]
    correct_line = "Once the saint of the Master,"
    assert generator.switch_words(line, "synonym", 5) == correct_line


def test_Paraphrase_switch_words_rhymes(monkeypatch):
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(example_poem)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[0]
    correct_line = "Loquacious Overlord, our grandchildren foresee,"
    assert generator.switch_words(line, "rhyme", 5) == correct_line


def test_Paraphrase_create_lyrics_synonyms(monkeypatch):
    example_poem = Lyrics(TEXT3)
    generator = Paraphrase(example_poem)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    correct_lyrics = """Thither is a sound, not tacit by complete,
Conveyed from these desert-caves. It is the boom
Of the take ice-cliff which the sunbeams bid,
Plunging into the vale--it is the fire
Descending on the pines--the torrents stream."""
    assert generator.create_lyrics("synonym") == correct_lyrics


def test_Paraphrase_create_lyrics_rhymes(monkeypatch):
    example_poem = Lyrics(TEXT4)
    generator = Paraphrase(example_poem)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    correct_lyrics = """His Part was darker none the starless knight
For but where is a morne
But in diss blackjack Receptacle
Can be no Abode of Don"""
    assert generator.create_lyrics("rhyme") == correct_lyrics
