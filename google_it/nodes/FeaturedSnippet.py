from utils.Constants import SELECTORS


class FeaturedSnippet:
    """Class representing a featured snippet."""

    def __init__(self, soup):
        """
        Initialize a new FeaturedSnippet object.

        Parameters:
        - soup (BeautifulSoup): BeautifulSoup object containing the HTML content.

        Attributes:
        - title (str | None): The title of the featured snippet.
        - description (str | None): The description of the featured snippet.
        - url (str | None): The URL associated with the featured snippet.
        """
        featured_snippet_title = (
                soup.select_one(SELECTORS.FEATURED_SNIPPET_TITLE[0]).text or
                soup.select_one(SELECTORS.FEATURED_SNIPPET_TITLE[1]).text or
                soup.select_one(SELECTORS.FEATURED_SNIPPET_TITLE[2]).text
        )

        featured_snippet_url = soup.select(SELECTORS.FEATURED_SNIPPET_URL)[0].get('href') if soup.select(
            SELECTORS.FEATURED_SNIPPET_URL) else None

        featured_snippet = [
            soup.select(selector)[0].get_text(strip=True)
            .replace('</li>', '')
            .replace('</b>', '')
            .replace('<b>', '')
            .replace('&amp;', '&')
            .replace('<li class="TrT0Xe">', '\n')
            for selector in SELECTORS.FEATURED_SNIPPET_DESC
            if soup.select(selector) and selector != SELECTORS.FEATURED_SNIPPET_DESC[2]
        ]

        self.title = featured_snippet_title if featured_snippet_title else None
        self.description = featured_snippet[0] if featured_snippet else None
        self.url = featured_snippet_url if featured_snippet_url else None
