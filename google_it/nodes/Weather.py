from utils import Constants


class Weather:
    """Class for representing weather information."""

    def __init__(self, soup, data):
        """
        Initialize a Weather object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.
        - data: String containing additional weather data.
        """
        weather_location = soup.select_one(Constants.SELECTORS.WEATHER_LOCATION).get_text().strip() if soup else None
        weather_forecast = soup.select_one(Constants.SELECTORS.WEATHER_FORECAST).get_text().strip() if soup else None
        precipitation = soup.select_one(Constants.SELECTORS.PRECIPITATION).get_text().strip() if soup else None
        air_humidity = soup.select_one(Constants.SELECTORS.AIR_HUMIDITY).get_text().strip() if soup else None
        temperature = soup.select_one(Constants.SELECTORS.TEMPERATURE).get_text().strip() if soup else None
        wind_speed = soup.select_one(Constants.SELECTORS.WIND_SPEED).get_text().strip() if soup else None

        is_available = weather_location and weather_forecast

        self.location = weather_location if is_available else None
        self.forecast = weather_forecast if is_available else None
        self.precipitation = precipitation if is_available else None
        self.humidity = air_humidity if is_available else None
        self.temperature = temperature if is_available else None
        self.wind = wind_speed if is_available else None

        # Extract image URL from data
        self.image = data.split('wob_tci')[1].split('var s=\'')[1].split('\';')[0] if is_available and 'wob_tci' in data else None
