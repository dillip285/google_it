from utils.constants import SELECTORS


class Converters:
    def __init__(self, soup):
        unit_converter_input = soup.select_one(SELECTORS.UNIT_CONVERTER_INPUT).get('value')
        unit_converter_output = soup.select_one(SELECTORS.UNIT_CONVERTER_OUTPUT).get('value')
        unit_converter_formula = soup.select_one(SELECTORS.UNIT_CONVERTER_FORMULA).text

        input_currency_name = soup.select_one(SELECTORS.INPUT_CURRENCY_NAME).get('data-name')
        output_currency_name = soup.select_one(SELECTORS.OUTPUT_CURRENCY_NAME).get('data-name')
        currency_converter_input = soup.select_one(SELECTORS.CURRENCY_CONVERTER_INPUT).text
        currency_converter_output = soup.select_one(SELECTORS.CURRENCY_CONVERTER_OUTPUT).text

        if unit_converter_input and unit_converter_output:
            self.input = unit_converter_input
            self.output = unit_converter_output
            self.formula = unit_converter_formula
        elif currency_converter_input and currency_converter_output:
            self.input = {
                'name': input_currency_name,
                'value': currency_converter_input
            }
            self.output = {
                'name': output_currency_name,
                'value': currency_converter_output
            }
