from song import Song
from lyrics import setup_config


CONFIG = setup_config("config.json")


def test_Song_create():
    # it comes through after reloading, something with api request
    author = "the weekend"
    title = "starboy"
    example_song = Song(CONFIG["urls"]["song"], author, title)
    lines = example_song.lyrics().split("\n")
    assert lines[1:] == CONFIG["test_text"]["song1"]["lines"]


def test_Song_search_song_wrong_artist():
    author = "dasdasdasdasdasd"
    title = "starboy"
    example_song = Song(CONFIG["urls"]["song"], author, title)
    assert example_song.lyrics() is None


def test_Song_search_song_wrong_title():
    author = "the weekend"
    title = "dasdasdsa"
    example_song = Song(CONFIG["urls"]["song"], author, title)
    assert example_song.lyrics() is None
