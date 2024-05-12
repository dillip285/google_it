from google_it.utils import Constants


class Converters:
    """Class for representing converters."""

    def __init__(self, soup):
        """
        Initialize a Converters object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.
        """
        if soup:
            unit_converter_input = getattr(soup.select_one(Constants.SELECTORS['UNIT_CONVERTER_INPUT']), 'value', None)
            unit_converter_output = getattr(soup.select_one(Constants.SELECTORS['UNIT_CONVERTER_OUTPUT']), 'value',
                                            None)
            unit_converter_formula = soup.select_one(
                Constants.SELECTORS['UNIT_CONVERTER_FORMULA']).get_text().strip() if soup.select_one(
                Constants.SELECTORS['UNIT_CONVERTER_FORMULA']) else None

            input_currency_name = getattr(soup.select_one(Constants.SELECTORS['INPUT_CURRENCY_NAME']), 'data-name',
                                          None)
            output_currency_name = getattr(soup.select_one(Constants.SELECTORS['OUTPUT_CURRENCY_NAME']), 'data-name',
                                           None)
            currency_converter_input = soup.select_one(
                Constants.SELECTORS['CURRENCY_CONVERTER_INPUT']).get_text().strip() if soup.select_one(
                Constants.SELECTORS['CURRENCY_CONVERTER_INPUT']) else None
            currency_converter_output = soup.select_one(
                Constants.SELECTORS['CURRENCY_CONVERTER_OUTPUT']).get_text().strip() if soup.select_one(
                Constants.SELECTORS['CURRENCY_CONVERTER_OUTPUT']) else None

            if unit_converter_input and unit_converter_output:
                self.input = unit_converter_input
                self.output = unit_converter_output
                self.formula = unit_converter_formula
            elif currency_converter_input and currency_converter_output:
                self.input = {'name': input_currency_name, 'value': currency_converter_input}
                self.output = {'name': output_currency_name, 'value': currency_converter_output}
        else:
            self.input = None
            self.output = None
            self.formula = None
