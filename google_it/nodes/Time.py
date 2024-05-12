from google_it.utils import Constants


class Time:
    """Class for representing current time."""

    def __init__(self, soup):
        """
        Initialize a Time object.

        Parameters:
        - soup: BeautifulSoup object.
        """
        hours = soup.select_one(Constants.SELECTORS['CURRENT_TIME_HOUR']).get_text().strip()
        dates = soup.select(Constants.SELECTORS['CURRENT_TIME_DATE'])
        date = None
        if len(dates) >= 2:
            date = dates[1].get_text().strip()  # Assuming the second date is the one we need

        self.hours = hours if date else None
        self.date = date if date else None
