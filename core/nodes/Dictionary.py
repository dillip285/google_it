from utils.constants import SELECTORS


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
        word = soup.select_one(SELECTORS.GD_WORD).text
        phonetic = soup.select_one(SELECTORS.GD_PHONETIC).text
        audio = soup.select_one(SELECTORS.GD_AUDIO).get('src') if soup.select_one(SELECTORS.GD_AUDIO) else None

        self.word = word if word else None
        self.phonetic = phonetic if word else None
        self.audio = f"https:{audio}" if word and audio else None
        self.definitions = [el.text for el in soup.select(SELECTORS.GD_DEFINITIONS)] if word else []
        self.examples = [el.text for el in soup.select(SELECTORS.GD_EXAMPLES)] if word else []
