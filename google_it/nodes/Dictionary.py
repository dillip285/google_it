from google_it.utils import Constants


class Dictionary:
    """Class representing a dictionary entry."""

    def __init__(self, soup):
        """
        Initialize a new Dictionary object.

        Parameters:
        - soup (BeautifulSoup): BeautifulSoup object containing the HTML content.

        Attributes:
        - word (str | None): The word being defined.
        - phonetic (str | None): Phonetic representation of the word.
        - audio (str | None): URL to the audio pronunciation.
        - definitions (list of str): List of definitions for the word.
        - examples (list of str): List of examples for the word.
        """
        if soup:
            word = getattr(soup.select_one(Constants.SELECTORS['GD_WORD']), 'text', None)
            phonetic = getattr(soup.select_one(Constants.SELECTORS['GD_PHONETIC']), 'text', None)
            audio = f"https:{getattr(soup.select_one(Constants.SELECTORS['GD_AUDIO']), 'get', lambda _: None)('src')}" if soup.select_one(
                Constants.SELECTORS['GD_AUDIO']) else None

            self.word = word
            self.phonetic = phonetic
            self.audio = audio
            self.definitions = [el.text for el in soup.select(Constants.SELECTORS['GD_DEFINITIONS'])]
            self.examples = [el.text for el in soup.select(Constants.SELECTORS['GD_EXAMPLES'])]
        else:
            self.word = None
            self.phonetic = None
            self.audio = None
            self.definitions = []
            self.examples = []
