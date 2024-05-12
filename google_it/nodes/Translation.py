from utils import Constants


class Translation:
    """Class for representing a translation."""

    def __init__(self, soup):
        """
        Initialize a Translation object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.
        """
        source_language = soup.select_one(Constants.SELECTORS.TR_SOURCE_LANGUAGE).get_text()
        target_language = soup.select_one(Constants.SELECTORS.TR_TARGET_LANGUAGE).get_text()

        source_text = soup.select_one(Constants.SELECTORS.TR_SOURCE_TEXT).get_text()
        target_text = soup.select_one(Constants.SELECTORS.TR_TARGET_TEXT).get_text()

        self.source_language = source_text if source_text else None
        self.target_language = target_language if source_text else None
        self.source_text = source_text if source_text else None
        self.target_text = target_text if target_text else None
