import lyricsgenius as lg
from urllib3 import exceptions


class Song:
    """
    This class fetches and formats song data from genius API.

    :param token: Genius API token
    :param type: str

    :param author: name of the song's artist
    :param type: str

    :param title: title of the song
    :param type: str

    :param lyrics: song lyrics
    :param type: str

    :param text: all song's data
    :param type: dict
    """
    def __init__(self, token, author, title):
        try:
            self.genius_object = lg.Genius(token, retries=50)
            self.genius_object.remove_section_headers = True
        except TimeoutError:
            pass
        self._lyrics = None
        self._text = self.search_song(author, title)

    def search_song(self, artist_name, title):
        """
        Search for song by artist and title. Return assign_values method.

        If artist_name, title or song object is empty returns None.
        """
        genius = self.genius_object
        song = None
        if artist_name and title:
            try:
                song = genius.search_song(title, artist_name)
            except exceptions.ReadTimeoutError:
                return None
            except TimeoutError:
                return None
            if song:
                return self.assign_values(song)
        return None

    def assign_values(self, song):
        """
        Formats song data.
        """
        text_dict = song.to_dict()
        self._lyrics = text_dict["lyrics"].strip("Embed1234567890")
        return text_dict

    def lyrics(self):
        """
        Return song lyrics.
        """
        return self._lyrics

    def get_text(self):
        """
        Return all data about song fetched from genius API.
        """
        return self._text
