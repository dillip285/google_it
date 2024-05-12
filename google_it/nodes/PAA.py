import json

from google_it.utils import Constants, Utils


class PAA:
    """Class for parsing People Also Ask (PAA) data."""

    @staticmethod
    def parse(soup, data):
        """
        Parse PAA data.

        Parameters:
        - soup: BeautifulSoup object.
        - data (str): Raw data containing PAA information.

        Returns:
        - List[str]: List of PAA items.
        """
        items = []

        # Extract PAA items from the specified selectors
        for item in Constants.SELECTORS['PAA']:
            for el in soup.select(item):
                items.append(el.text)

        # Remove the first item as it's not part of the PAA section
        items.pop(0)

        # Extract additional data from the raw data string
        extra_data = json.loads(Utils.get_string_between_strings(data, 'var c=\'', '\';google') or '{}')
        rfs = extra_data.get('sb_wiz', {}).get('rfs', [])

        # Process and add additional PAA items
        for el in rfs:
            items.append(el.replace('<b>', '').replace('</b>', ''))

        return items
