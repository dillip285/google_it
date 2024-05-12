from google_it.nodes.MetadataItem import MetadataItem
from google_it.nodes.Social import Social
from google_it.utils import Utils
from google_it.utils.Constants import SELECTORS


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

        self.title = self._get_title(soup)
        self.description = self._get_description(soup)
        self.url = self._get_url(soup)
        self.metadata = self._get_metadata(soup)
        self.type = self._get_type(soup)
        self.books = self._get_books(soup)
        self.tv_shows_and_movies = self._get_tv_shows_and_movies(soup)
        self.lyrics = self._get_lyrics(soup)
        self.ratings = self._get_ratings(soup)
        self.available_on = self._get_available_on(soup)
        self.images = self._get_images(soup)
        self.songs = self._get_songs(soup)
        self.socials = self._get_socials(soup)
        self.demonstration = self._get_demonstration(data)  # Implement if needed

    def _get_title(self, soup):
        """Extracts title from the knowledge panel."""
        title = None
        for selector in SELECTORS['KNO_PANEL_TITLE']:
            element = soup.select_one(selector)
            if element:
                title = element.text.strip() or None
                break
        return title

    def _get_description(self, soup):
        """Extracts description from the knowledge panel."""
        description = None
        for selector in SELECTORS['KNO_PANEL_DESCRIPTION']:
            element = soup.select_one(selector)
            if element:
                if element.find("span"):
                    description = element.find("span").text.strip() or None
                else:
                    description = element.text.strip() or None
                break
        return description

    def _get_url(self, soup):
        """Extracts URL from the knowledge panel."""
        url = soup.select_one(SELECTORS['KNO_PANEL_URL'])
        if url:
            return url.get("href")
        else:
            description_element = soup.select_one(SELECTORS['KNO_PANEL_DESCRIPTION'][1])
            if description_element and description_element.find("a"):
                return description_element.find("a").get("href")
        return None

    # Implement similar methods for _get_metadata, _get_type, etc. following the pattern above

    def _get_metadata(self, soup):
        metadata = []
        elements = soup.select(SELECTORS['KNO_PANEL_METADATA'])
        for index in range(0, len(elements), 2):
            key = elements[index].text.strip()[:-1]
            value = elements[index+1].text.strip()
            if value:
                metadata.append(MetadataItem(key, value))
        return metadata

    def _get_type(self, soup):
        knowledge_panel_type = soup.select_one(SELECTORS['KNO_PANEL_TYPE'])
        if knowledge_panel_type:
            type_text = knowledge_panel_type.text.strip()
            if type_text != self.title:
                return type_text
        return None

    def _get_books(self, soup):
        books = []
        for element in soup.select(SELECTORS['KNO_PANEL_BOOKS']):
            title_element = element.find_previous_sibling().find("div").find("span")
            if title_element:
                title = title_element.text.strip()
            else:
                title = None
            year = element.find_next_sibling().text.strip()
            if year:
                books.append({"title": title, "year": year})
        return books

    def _get_tv_shows_and_movies(self, soup):
        # Similar logic to _get_books
        tv_shows_and_movies = []
        for element in soup.select(SELECTORS['KNO_PANEL_TV_SHOWS_AND_MOVIES']):
            title_element = element.find_previous_sibling().find("div").find("span")
            if title_element:
                title = title_element.text.strip()
            else:
                title = None
            year = element.find_next_sibling().text.strip()
            if year:
                tv_shows_and_movies.append({"title": title, "year": year})
        return tv_shows_and_movies

    def _get_lyrics(self, soup):
        lyrics_elements = soup.select(SELECTORS['KNO_PANEL_SONG_LYRICS'])
        lyrics = []
        for element in lyrics_elements:
            html = element.text.strip()
            # Process HTML to plain text with newline characters
            lyrics.append(html.replace("<br aria-hidden=\"true\">", "\n")
                          .replace("</span></div><div jsname=\".*\" class=\".*\"><span jsname=\".*\">", "\n\n")
                          .replace("<br>", "\n"))
        return "\n\n".join(lyrics) if lyrics else None

    def _get_ratings(self, soup):
        ratings = []
        google_users_rating = soup.select_one(SELECTORS['KNO_PANEL_FILM_GOOGLEUSERS_RATING'])
        if google_users_rating:
            rating = google_users_rating.find_all("text")[0].strip() or None
            ratings.append({"name": "Google Users", "rating": rating})

        for i, element in enumerate(soup.select(SELECTORS['KNO_PANEL_FILM_RATINGS'][0])):
            name = soup.select_one(SELECTORS['KNO_PANEL_FILM_RATINGS'][1])[i].get("title")
            rating = element.text.strip()
            ratings.append({"name": name, "rating": rating})
        return ratings

    def _get_available_on(self, soup):
        return [element.text.strip() for element in soup.select(SELECTORS['KNO_PANEL_AVAILABLE_ON'])]

    def _get_images(self, soup):
        images = []
        for element in soup.select(SELECTORS['KNO_PANEL_IMAGES']):
            url = element.get("data-src")
            source = element.parent.parent.parent.parent.parent.get("data-lpage")
            if url:
                images.append({"url": url, "source": source})
        return images

    def _get_songs(self, soup):
        songs = []
        for element in soup.select(SELECTORS['KNO_PANEL_SONGS']):
            title = element.text.strip()
            album = element.find_next_sibling().find("span").text.strip()
            songs.append({"title": title, "album": album})
        return songs

    def _get_socials(self, soup):
        socials = []
        for element in soup.select(SELECTORS['KNO_PANEL_SOCIALS']):
            name = element.text.strip()
            url = element.get("href")
            icon = element.find("img").get("src")
            socials.append(Social(name, url, icon))
        return socials

    def _get_demonstration(self, data):
        return Utils.get_string_between_strings(data, 'source src\\x3d\\x22',
                                                '.mp4') + '.mp4' if Utils.get_string_between_strings(data,
                                                                                                     'source src\\x3d\\x22',
                                                                                                     '.mp4') else None
