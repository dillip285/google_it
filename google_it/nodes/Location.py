from google_it.utils.Constants import SELECTORS


class Location:
    """Class representing a location."""

    def __init__(self, soup):
        """
        Initialize a new Location object.

        Parameters:
        - soup (BeautifulSoup): BeautifulSoup object containing the HTML content.

        Attributes:
        - title (str | None): The title of the location.
        - distance (str | None): The distance of the location.
        - map (str | None): The URL of the map image of the location.
        """
        location_title = soup.select_one(SELECTORS['LOCATION_TITLE']).get_text(strip=True) if soup.select_one(
            SELECTORS['LOCATION_TITLE']) else None
        location_distance = soup.select_one(SELECTORS['LOCATION_DISTANCE']).get_text(strip=True) if soup.select_one(
            SELECTORS['LOCATION_DISTANCE']) else None
        location_image = soup.select_one(SELECTORS['LOCATION_IMAGE']).get('src') if soup.select_one(
            SELECTORS['LOCATION_IMAGE']) else None

        is_available = location_title and location_distance

        self.title = location_title if is_available else None
        self.distance = location_distance if is_available else None
        self.map = f"https://google.com/{location_image}" if is_available else None
