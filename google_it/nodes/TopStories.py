from utils import Constants


class Item:
    """Class for representing an item."""

    def __init__(self, data):
        """
        Initialize an Item object.

        Parameters:
        - data: Dictionary containing item data.
        """
        self.description = data.get('description')
        self.url = data.get('url')


class TopStories:
    @staticmethod
    def parse(soup):
        """
        Parse the top stories from the given BeautifulSoup object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.

        Returns:
        - List of Item objects representing the top stories.
        """
        # Removes unwanted text from the description
        for selector in Constants.SELECTORS.TOP_STORIES_DESCRIPTION:
            for el in soup.select(selector):
                el.extract()

        top_stories_descriptions = [
            el.get_text() for selector in Constants.SELECTORS.TOP_STORIES_DESCRIPTION
            for el in soup.select(selector)
        ]
        top_stories_urls = [
            el['href'] for el in soup.select(Constants.SELECTORS.TOP_STORIES_URL)
        ]

        items = []
        for description, url in zip(top_stories_descriptions, top_stories_urls):
            items.append(Item({'description': description, 'url': url}))

        return items
