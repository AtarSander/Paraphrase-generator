from lyrics import Lyrics

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


def test_Lyrics__str__():
    example_poem = Lyrics(TEXT2)
    assert str(example_poem) == "\n".join(TEXT2[0]["lines"])


def test_Lyrics_author():
    example_poem = Lyrics(TEXT2)
    assert example_poem.author() == "William Cowper"


def test_Lyrics_title():
    example_poem = Lyrics(TEXT2)
    assert example_poem.title() == "Prayer for Children"


def test_Lyrics_lines():
    example_poem = Lyrics(TEXT2)
    assert example_poem.lines() == TEXT2[0]["lines"]
