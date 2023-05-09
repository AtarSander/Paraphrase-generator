### Project description
The program allows for simple paraphrasing of texts based on criteria selected in the user interface. Three text replacement methods are implemented (rhyme substitution, synonym replacement, expansion of description with additional adjectives). Each of these methods can be applied to the first, last, random, or every word in a line. The user can also adjust the accuracy and diversity of the changed words. The user can search for song lyrics or generate a random verse as the text to be paraphrased.

### Interface
The Interface class in the interface.py file is responsible for handling the interface. After starting the program, the main menu is displayed in the console, and the user navigates it by entering numbers corresponding to the individual options. The user can choose the help option, text generation, paraphrase generation, saving the paraphrase to the database, searching for a paraphrase in the database, or closing the program.

1. The help option displays a longer description of each of the main options and allows for detailed help for two more complex options.
2. Text generation allows the user to search for song lyrics by providing the author and title through the Genius API or generate a random verse from the PoetryDB API.
3. Paraphrase generation, after configuring the text replacement method, word position in the line, and accuracy of substitution, paraphrases the previously generated text and displays it with the replaced words highlighted.
4. The next option saves the paraphrase to the database (dictionary, with the key of each paraphrase being its title).
5. Saved paraphrases can be searched and displayed by entering the original text's title for the corresponding paraphrase.
6. The last option ends the program.
### Lyrics
The setup_config function is responsible for loading the configuration file, and the get_text function is responsible for retrieving data from the API. The Lyrics class formats and stores the song's text along with the title and author. The above functions and classes are in the lyrics.py file.

### Song
The Song class in the song.py file is responsible for retrieving data from the Genius API and processing it into the appropriate format.

### Paraphrase
The Paraphrase class in the paraphrase.py file is responsible for the logic of converting text into a paraphrase.
- After receiving the text to be processed and the replacement specifications in the constructor, it is processed line by line.
- The word in the appropriate line position (according to the change parameter) is sent to a method that retrieves a list of responses from the Datamuse API for that word based on the criteria of the given text replacement method (according to the option parameter). The list's length is determined by the user (according to the variety parameter [responses in the API are sorted from most to least suitable, so a smaller number of responses provides greater accuracy of substitution, but a larger number reduces the risk of repetition but decreases paraphrase accuracy]).
- Next, a random word is selected from the list of responses, its punctuation and color are corrected to display it in green in the console.
- This word replaces the original word in the line for the rhyme and synonym options or is "inserted" before the original word for the adjective addition option.
- A similar algorithm is performed for all subsequent lines of text.
- If no match is found for the query in the Datamuse API, the original word remains in its place.

To maintain minimal paraphrase accuracy, even for complex sentences, the program breaks down sentences into individual lines, paraphrases them, and then combines them back into a sentence.
This excludes interference with words such as "I", "you", "we", "he", "she", "the", and the like, the violation of which would completely change the content of the verse.
### Summary
The main project objectives have been achieved:
- The program generates text by searching for the user or randomly
- The user can paraphrase the generated text using three different methods, changing the first, last, random, or all words in the verse, adjusting the diversity and accuracy at the same time
- Generated paraphrases with highlighted green replaced or added words can be saved in the database and easily searched
Unfortunately, it was not possible to significantly reduce the time it takes to generate a paraphrase. Although the difference between replacing all words and replacing one word in the line is very large, the second option can still take several seconds for a slightly longer text. This is due to multiple API queries, so it is difficult to optimize this functionality.
The program only works for texts in English. The Genius API supports Polish and most other languages, but PoetryDB and, more importantly, Datamuse are exclusively in English. If these APIs were to add support for other languages in the future, adapting the program to them would only require changing 2-3 lines in the configuration file.
A paraphrase is a modification of a work while preserving its meaning, which somewhat limits the ability to interfere with the text. However, the project described could successfully change the text in other ways, such as using antonyms, homonyms, words associated with a particular word, etc. Such a change would be a matter of adding a few lines to the configuration file and naming a new option. Therefore, the project adheres to the open-close principle.