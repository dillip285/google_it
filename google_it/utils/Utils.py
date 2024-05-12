import datetime
import json
import os
import random
import re

from bs4 import BeautifulSoup


class SearchError(Exception):
    def __init__(self, message, info=None):
        super().__init__(message)
        self.info = info
        self.date = datetime.now()
        self.version = __import__("../../package.json")['version']


def get_headers(options={'mobile': False}):
    user_agents = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user-agents.json')))
    selected_agent = 'mobile' if options['mobile'] else 'desktop'
    available_agents = user_agents[selected_agent]
    ua = random.choice(available_agents)
    return {
        'accept': 'text/html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en',
        'referer': 'https://www.google.com/',
        'user-agent': ua
    }


def refine_data(data, parse_ads=False, is_mobile=True):
    result = data

    result = re.sub(b'N6jJud VwiC3b lyLwlc|YjtGef ExmHv VwiC3b|VwiC3b lyLwlc aLF0Z', b'', result)
    result = re.sub(b'yDYNvb lEBKkf', b'yDYNvb', result)
    result = re.sub(b'VwiC3b yDYNvb', b'MUxGbd yDYNvb', result)
    result = re.sub(b'VwiC3b MUxGbd yDYNvb', b'MUxGbd yDYNvb', result)
    result = re.sub(b'cz3goc BmP5tf', b'C8nzq BmP5tf', result)
    result = re.sub(b'cz3goc v5yQqb BmP5tf', b'C8nzq BmP5tf', result)
    result = re.sub(b'ynAwRc q8U8x MBeuO oewGkc LeUQr', b'ynAwRc q8U8x MBeuO gsrt oewGkc LeUQr', result)
    result = re.sub(b'MBeuO oewGkc', b'MBeuO gsrt oewGkc', result)

    if not is_mobile:
        result = re.sub(b'yuRUbf|v5yQqb', b'ynAwRc q8U8x MBeuO gsrt oewGkc LeUQr', result)

    if parse_ads:
        result = re.sub(b'cz3goc v5yQqb BmP5tf', b'C8nzq BmP5tf', result)

    return result


def get_string_between_strings(data, start_string, end_string):
    soup = BeautifulSoup(data, 'html.parser')
    text = soup.get_text()
    regex = re.compile(f'{re.escape(start_string)}(.*?){re.escape(end_string)}', re.DOTALL)
    match = regex.search(text)
    return match.group(1) if match else None


def generate_random_string(length):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    return ''.join(random.choice(alphabet) for _ in range(length))


def get_random_int(min, max):
    return random.randint(min, max)

