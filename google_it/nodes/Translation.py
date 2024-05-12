from google_it.utils import Constants

class Translation:
    """Class for representing a translation."""

    def __init__(self, soup):
        """
        Initialize a Translation object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.
        """
        source_language = soup.select_one(Constants.SELECTORS['TR_SOURCE_LANGUAGE']).get_text() if soup.select_one(Constants.SELECTORS['TR_SOURCE_LANGUAGE']) else None
        target_language = soup.select_one(Constants.SELECTORS['TR_TARGET_LANGUAGE']).get_text() if soup.select_one(Constants.SELECTORS['TR_TARGET_LANGUAGE']) else None

        source_text = soup.select_one(Constants.SELECTORS['TR_SOURCE_TEXT']).get_text() if soup.select_one(Constants.SELECTORS['TR_SOURCE_TEXT']) else None
        target_text = soup.select_one(Constants.SELECTORS['TR_TARGET_TEXT']).get_text() if soup.select_one(Constants.SELECTORS['TR_TARGET_TEXT']) else None

        self.source_language = source_language
        self.target_language = target_language
        self.source_text = source_text
        self.target_text = target_text
