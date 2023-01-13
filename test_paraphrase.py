from paraphrase import Paraphrase
from lyrics import Lyrics, setup_config
import random


test_texts = setup_config("config.json", "test_text")
CONFIG = setup_config("config.json", "urls")
TEXT1 = test_texts["text1_medium"]
TEXT2 = test_texts["text2_short"]
TEXT3 = test_texts["text3_short"]
TEXT4 = test_texts["text4_medium"]
TEXT5 = test_texts["text5_short"]


def test_Paraphrase_correct_upper_capitalize():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem)
    assert generator.correct_upper("Gracious", "good") == "Good"


def test_Paraphrase_correct_upper_all():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem)
    assert generator.correct_upper("GRACIOUS", "good") == "GOOD"


def test_Paraphrase_correct_punctuation_end():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem)
    assert generator.correct_punctuation("sword,", "blade") == "blade,"


def test_Paraphrase_correct_punctuation_start():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem)
    assert generator.correct_punctuation("(sword", "blade") == "(blade"


def test_Paraphrase_correct_punctuation_both():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem)
    assert generator.correct_punctuation("(sword,", "blade") == "(blade,"


def test_Paraphrase_choose_words_synonyms():
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "all", 6)
    assert generator.choose_words("gracious") == ["good",
                                                  "kind",
                                                  "nice",
                                                  "benevolent",
                                                  "elegant",
                                                  "propitious"]


def test_Paraphrase_choose_words_rhymes():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "all", 4)
    assert generator.choose_words("pour") == ["for",
                                              "pore",
                                              "tor",
                                              "outpour"]


def test_Paraphrase_choose_words_adjectives():
    pass


def test_Paraphrase_switch_words_synonyms_all(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "all", 5)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[9]
    correct_line = "Once the saint of the Master,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_synonyms_last(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "last", 5)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[9]
    correct_line = "When the angel of the Master,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_synonyms_first(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "first", 5)

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[9]
    correct_line = "Once the angel of the Lord,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_synonyms_random(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "random", 5)

    def mock_choice(data):
        return data[3]
    monkeypatch.setattr(random, "choice", mock_choice)

    line = example_poem.lines()[10]
    correct_line = "Drawing forth his awful sword,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_rhymes_all(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "all")

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[0]
    correct_line = "Loquacious Overlord, our grandchildren foresee,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_rhymes_last(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "last")

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[0]
    correct_line = "Gracious Lord, our children foresee,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_rhymes_first(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "first")

    def mock_choice(data):
        return data[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[10]
    correct_line = "Withdrawing forth his dreadful sword,"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_switch_words_rhymes_random(monkeypatch):
    example_poem = Lyrics(TEXT3)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "random", 5)

    def mock_choice(data):
        return data[1]
    monkeypatch.setattr(random, "choice", mock_choice)
    line = example_poem.lines()[0]
    correct_line = "His Tart was darker than the starless night"
    assert generator.switch_words(line) == correct_line


def test_Paraphrase_insert_adjective(monkeypatch):
    example_poem = Lyrics(TEXT1)
    generator = Paraphrase(CONFIG, example_poem, "adjective", "first", 1)
    line = example_poem.lines()[0]
    line = line.split()
    correct_line = "Good gracious Lord, our children see,"
    assert " ".join(generator.insert_adjective(line, 0)) == correct_line


def test_Paraphrase_create_lyrics_synonyms_all():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "all", 1)
    correct_lyrics = """Thither is a sound, not tacit by complete,
Conveyed from these desert-caves. It is the boom
Of the take ice-cliff which the sunbeams bid,
Plunging into the vale--it is the fire
Descending on the pines--the torrents stream."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_synonyms_first():
    example_poem = Lyrics(TEXT4)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "first", 1)
    correct_lyrics = """World affects to be sedate
Upon occasion, grand
But let our observation shut
Her practices extend

To Necromancy and the Trades
Far to understand
Lay eyes on our spacious Citizen
Unto a Juggler turned --"""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_synonyms_last():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "last", 1)
    correct_lyrics = """There is a voice, not understood by complete,
Sent from these desert-caves. It is the boom
Of the rent ice-cliff which the sunbeams bid,
Plunging into the vale--it is the fire
Descending on the pines--the torrents stream."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_synonyms_random(monkeypatch):
    example_poem = Lyrics(TEXT5)
    generator = Paraphrase(CONFIG, example_poem, "synonym", "random")

    def mock_choice(words):
        if not words:
            return ""
        elif len(words) > 1:
            return words[1]
        else:
            return words[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    correct_lyrics = """The Mount sat upon the Plain
In his tremendous Chair --
His reflection omnifold,
His inquest, everywhere --\n
The Seasons played around his knees
Like Children round a sire --
Grandfather of the Days is He
Of Penetrate, the Ancestor --"""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_rhymes_all():
    example_poem = Lyrics(TEXT3)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "all", 1)
    correct_lyrics = """His Part was darker none the starless knight
For but where is a morne
But in diss blackjack Receptacle
Can be no Abode of Don"""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_rhymes_last():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "last", 1)
    correct_lyrics = """There is a voice, not understood by overall,
Sent from these desert-caves. It is the fore
Of the rent ice-cliff which the sunbeams recall,
Plunging into the vale--it is the past
Descending on the pines--the torrents for."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_rhymes_first():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "first", 1)
    correct_lyrics = """Where is a voice, not understood by all,
Went from these desert-caves. It is the roar
Of the rent ice-cliff which the sunbeams call,
Plunging into the vale--it is the blast
Ascending on the pines--the torrents pour..."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_rhymes_random(monkeypatch):
    example_poem = Lyrics(TEXT5)
    generator = Paraphrase(CONFIG, example_poem, "rhyme", "random")

    def mock_choice(words):
        if not words:
            return ""
        elif len(words) > 1:
            return words[1]
        else:
            return words[0]
    monkeypatch.setattr(random, "choice", mock_choice)
    correct_lyrics = """The Mountain sat upon the Plain
In his tremendous Chair --
His consideration omnifold,
His quest, everywhere --\n
The Seasons played around his knees
Like Schoolchildren round a sire --
Grandfather of the Days is He
Of Predawn, the Ancestor --"""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_adjectives_all():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "adjective", "all", 1)
    correct_lyrics = """Getting there is a low voice, not little understood by cell all,
Haughty sent letter from try these desert-caves. It is the deafening roar
Of the annual rent ice-cliff new which the golden sunbeams first call,
Deep plunging dissolve into the vale--it is the full blast
Own descending on the pines--the such torrents pece pour..."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_adjectives_last():
    example_poem = Lyrics(TEXT2)
    generator = Paraphrase(CONFIG, example_poem, "adjective", "last", 1)
    correct_lyrics = """There is a voice, not understood by cell all,
Sent from these desert-caves. It is the deafening roar
Of the rent ice-cliff which the sunbeams first call,
Plunging into the vale--it is the full blast
Descending on the pines--the torrents pece pour..."""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_adjectives_first():
    example_poem = Lyrics(TEXT4)
    generator = Paraphrase(CONFIG, example_poem, "adjective", "first", 1)
    correct_lyrics = """Human nature affects to be sedate
Agreed upon occasion, grand
But let our observation shut
Her practices extend\n
To Necromancy and the Trades
Immense remote to understand
Young behold our spacious Citizen
Same unto a Juggler turned --"""
    assert generator.create_lyrics() == correct_lyrics


def test_Paraphrase_create_lyrics_adjectives_random(monkeypatch):
    example_poem = Lyrics(TEXT4)
    generator = Paraphrase(CONFIG, example_poem, "adjective", "random")

    def mock_choice(data):
        return data[1]
    monkeypatch.setattr(random, "choice", mock_choice)
    correct_lyrics = """Nature positive affects to be sedate
Upon present occasion, grand
But let our observation shut
Her best practices extend\n
To such Necromancy and the Trades
Remote to understand
Behold our spacious Citizen
Unto a Juggler turned --"""
    assert generator.create_lyrics() == correct_lyrics
