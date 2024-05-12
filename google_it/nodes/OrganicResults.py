from urllib.parse import urlparse

from utils import Constants
from utils.Constants import SELECTORS


class OrganicResult:
    """Class representing an organic search result."""

    def __init__(self, title, description, url, is_sponsored, favicons):
        """
        Initialize a new OrganicResult object.

        Parameters:
        - title (str): The title of the search result.
        - description (str): The description of the search result.
        - url (str): The URL of the search result.
        - is_sponsored (bool): Indicates if the search result is sponsored.
        - favicons (dict): Dictionary containing URLs for high and low resolution favicons.
        """
        self.title = title
        self.description = description
        self.url = url
        self.is_sponsored = is_sponsored
        self.favicons = favicons


class OrganicResults:
    """Class for parsing organic search results."""

    @staticmethod
    def parse(soup, parse_ads=False, is_mobile=True):
        """
        Parse organic search results from BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): BeautifulSoup object containing the HTML content.
        - parse_ads (bool): Whether to parse sponsored results or not.
        - is_mobile (bool): Whether the search is done from a mobile device or not.

        Returns:
        - list[OrganicResult]: List of parsed organic search results.
        """
        ad_indexes = []

        titles = [el.get_text(strip=True) for el in soup.select(SELECTORS.TITLE)]
        descriptions = [el.get_text(strip=True) for el in soup.select(SELECTORS.DESCRIPTION)]
        urls = [el.get('href') for el in soup.select(SELECTORS.URL if is_mobile else f"{SELECTORS.TITLE} > a")]

        if len(titles) < len(urls):
            urls.pop(0)

        if len(urls) > len(titles):
            urls.pop(0)

        is_inaccurate_data = len(descriptions) < len(urls[1:])

        for i, url in enumerate(urls):
            if url and (url.startswith('/aclk') or url.startswith('/amp/s')):
                urls[i] = f"{Constants.URLS.W_GOOGLE}{url[1:]}"

        results = []

        for i, (title, description, url) in enumerate(zip(titles, descriptions, urls)):
            if url and (title or description):
                high_res_favicon = f"{Constants.URLS.FAVICONKIT}/{urlparse(url).hostname}/192"
                low_res_favicon = f"{Constants.URLS.W_GOOGLE}s2/favicons?sz=64&domain_url={urlparse(url).hostname}"

                results.append(OrganicResult(title, description, url, i in ad_indexes,
                                             {"high_res": high_res_favicon, "low_res": low_res_favicon}))

        return results
