import datetime
import random
import re


class SearchError(Exception):
    def __init__(self, message, info=None):
        super().__init__(message)
        self.info = info
        self.date = datetime.now()
        self.version = __import__("../../package.json")['version']


def get_headers(options={'mobile': False}):
    user_agents = __import__('./user-agents.json')
    available_agents = user_agents['mobile' if options['mobile'] else 'desktop']
    ua = random.choice(available_agents)
    return {
        'accept': 'text/html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en',
        'referer': 'https://www.google.com/',
        'upgrade-insecure-requests': 1,
        'user-agent': ua
    }


def refine_data(data, parse_ads=False, is_mobile=True):
    result = data
    result = re.sub(r'N6jJud VwiC3b lyLwlc|YjtGef ExmHv VwiC3b|VwiC3b lyLwlc aLF0Z', '', result)
    result = re.sub(r'yDYNvb lEBKkf', 'yDYNvb', result)
    result = re.sub(r'VwiC3b yDYNvb', 'MUxGbd yDYNvb', result)
    result = re.sub(r'VwiC3b MUxGbd yDYNvb', 'MUxGbd yDYNvb', result)
    result = re.sub(r'cz3goc BmP5tf', 'C8nzq BmP5tf', result)
    result = re.sub(r'cz3goc v5yQqb BmP5tf', 'C8nzq BmP5tf', result)
    result = re.sub(r'ynAwRc q8U8x MBeuO oewGkc LeUQr', 'ynAwRc q8U8x MBeuO gsrt oewGkc LeUQr', result)
    result = re.sub(r'MBeuO oewGkc', 'MBeuO gsrt oewGkc', result)

    if not is_mobile:
        result = re.sub(r'yuRUbf|v5yQqb', 'ynAwRc q8U8x MBeuO gsrt oewGkc LeUQr', result)

    if parse_ads:
        result = re.sub(r'cz3goc v5yQqb BmP5tf', 'C8nzq BmP5tf', result)

    return result


def get_string_between_strings(data, start_string, end_string):
    regex = re.compile(f'{re.escape(start_string)}(.*?){re.escape(end_string)}', re.DOTALL)
    match = regex.search(data)
    return match.group(1) if match else None


def generate_random_string(length):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    return ''.join(random.choice(alphabet) for _ in range(length))


def get_random_int(min, max):
    return random.randint(min, max)

