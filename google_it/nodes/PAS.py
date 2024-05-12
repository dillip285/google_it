from google_it.utils import Constants


class Query:
    """Class representing a query with title and thumbnail."""

    def __init__(self, title, thumbnail):
        """
        Initialize a Query object.

        Parameters:
        - title (str): The title of the query.
        - thumbnail (str): The URL of the thumbnail.
        """
        self.title = title
        self.thumbnail = thumbnail


class PAS:
    """Class for parsing People Also Search (PAS) data."""

    @staticmethod
    def parse(soup):
        """
        Parse PAS data.

        Parameters:
        - soup: BeautifulSoup object.

        Returns:
        - List[Query]: List of Query objects representing PAS items.
        """
        items = []

        # Iterate over each PAS item and extract title and thumbnail
        for el in soup.select(Constants.SELECTORS['PASF']):
            data_src = el.get('data-src')
            alt = el.get('alt')
            if data_src:
                items.append(Query(title=alt, thumbnail=f"https:{data_src}"))

        return items
