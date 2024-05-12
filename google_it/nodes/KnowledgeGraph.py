import MetadataItem
import Social
from utils import Utils
from utils.Constants import SELECTORS


class KnowledgeGraph:
    """Class representing a knowledge graph."""

    def __init__(self, data, soup):
        """
        Initialize a new KnowledgeGraph object.

        Parameters:
        - data (str): Raw data string.
        - soup (BeautifulSoup): BeautifulSoup object containing the HTML content.

        Attributes:
        - type (str | None): The type of the knowledge graph.
        - title (str | None): The title of the knowledge graph.
        - description (str | None): The description of the knowledge graph.
        - url (str | None): The URL associated with the knowledge graph.
        - metadata (list of MetadataItem): List of metadata items.
        - books (list of dict): List of books associated with the knowledge graph.
        - tv_shows_and_movies (list of dict): List of TV shows and movies associated with the knowledge graph.
        - ratings (list of dict): List of ratings associated with the knowledge graph.
        - available_on (list of str): List of platforms where the knowledge graph is available.
        - images (list of dict): List of images associated with the knowledge graph.
        - songs (list of dict): List of songs associated with the knowledge graph.
        - socials (list of Social): List of social media links associated with the knowledge graph.
        - demonstration (str | None): The URL of the demonstration video associated with the knowledge graph.
        - lyrics (str | None): The lyrics associated with the knowledge graph.
        """
        self.title = soup.select_one(SELECTORS.KNO_PANEL_TITLE[0]).text or \
                     soup.select_one(SELECTORS.KNO_PANEL_TITLE[1]).text or \
                     None

        self.description = soup.select_one(SELECTORS.KNO_PANEL_DESCRIPTION[0]).text or \
                           soup.select_one(SELECTORS.KNO_PANEL_DESCRIPTION[1]).find('span').text or \
                           None

        self.url = soup.select_one(SELECTORS.KNO_PANEL_URL).get('href') or \
                   soup.select_one(SELECTORS.KNO_PANEL_DESCRIPTION[1]).find('a').get('href') or \
                   None

        self.metadata = [MetadataItem({'title': el.get_text(strip=True), 'value': el.find_next().get_text(strip=True)})
                         for el in soup.select(SELECTORS.KNO_PANEL_METADATA)]

        self.type = soup.select(SELECTORS.KNO_PANEL_TYPE)[-1].get_text() if soup.select(
            SELECTORS.KNO_PANEL_TYPE) else None

        self.books = [{'title': el.find_previous('div').find('span').text.strip(), 'year': el.get_text(strip=True)} for
                      el in soup.select(SELECTORS.KNO_PANEL_BOOKS) if el.get_text(strip=True)]

        self.tv_shows_and_movies = [
            {'title': el.find_previous('div').find('span').text.strip(), 'year': el.get_text(strip=True)} for el in
            soup.select(SELECTORS.KNO_PANEL_TV_SHOWS_AND_MOVIES) if el.get_text(strip=True)]

        self.lyrics = '\n\n'.join([el.get_text() for el in soup.select(SELECTORS.KNO_PANEL_SONG_LYRICS)]) or None

        self.ratings = [{'name': 'Google Users', 'rating': soup.select_one(
            SELECTORS.KNO_PANEL_FILM_GOOGLEUSERS_RATING).get_text()}] if soup.select_one(
            SELECTORS.KNO_PANEL_FILM_GOOGLEUSERS_RATING) else []
        self.ratings += [{'name': el.get('title'), 'rating': el.get_text()} for el in
                         soup.select(SELECTORS.KNO_PANEL_FILM_RATINGS[0])]

        self.available_on = [el.get_text(strip=True) for el in soup.select(SELECTORS.KNO_PANEL_AVAILABLE_ON)]

        self.images = [{'url': el.get('data-src'),
                        'source': el.find_parent().find_parent().find_parent().find_parent().find_parent().get(
                            'data-lpage')} for el in soup.select(SELECTORS.KNO_PANEL_IMAGES) if el.get('data-src')]

        self.songs = [{'title': el.get_text(strip=True), 'album': el.find_next('span').text.strip()} for el in
                      soup.select(SELECTORS.KNO_PANEL_SONGS)]

        self.socials = [Social({'name': el.get_text(), 'url': el.get('href'), 'icon': el.find('img').get('src')}) for el
                        in soup.select(SELECTORS.KNO_PANEL_SOCIALS)]

        self.demonstration = Utils.get_string_between_strings(data, 'source src\\x3d\\x22',
                                                              '.mp4') + '.mp4' if Utils.get_string_between_strings(data,
                                                                                                                   'source src\\x3d\\x22',
                                                                                                                   '.mp4') else None
