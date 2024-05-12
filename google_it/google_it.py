import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
import random

from nodes import (
    OrganicResults, KnowledgeGraph, FeaturedSnippet,
    Location, Translation, Dictionary, Videos, TopStories, Weather, Time, PAA, PAS, Converters
)
from utils import Constants
from utils import Utils


def search(query, options={}):
    response = None

    ris = options.get('ris', False)
    safe = options.get('safe', False)
    page = options.get('page', 0) * 10 if 'page' in options else 0
    use_mobile_ua = options.get('use_mobile_ua', True)
    parse_ads = options.get('parse_ads', False)
    additional_params = options.get('additional_params', {})
    axios_config = options.get('axios_config', {})

    if isinstance(query, dict) and ris:
        response = upload_image(query, axios_config)
    else:
        _query = urlencode({'q': query})

        if ris:
            raise Utils.SearchError(
                'Reverse image search by URL has been deprecated by Google. Please use a file instead.')

        url = f"{Constants.URLS.GOOGLE}search?{_query}&ie=UTF-8&aomd=1{'&safe=active' if safe else ''}&start={page}"
        response = requests.get(url, params=additional_params, headers=Utils.get_headers(mobile=use_mobile_ua),
                                **axios_config)

    if response is None or response.status_code != 200:
        raise Utils.SearchError('Could not execute search',
                                status_code=response.status_code if response is not None else 0)

    soup = BeautifulSoup(Utils.refine_data(response.content, parse_ads, use_mobile_ua), 'html.parser')

    # Result Dictionary
    results = {}

    results['results'] = OrganicResults.parse(soup, parse_ads, use_mobile_ua)
    results['videos'] = Videos.parse(soup)

    results['knowledge_panel'] = KnowledgeGraph(response.content, soup)
    results['featured_snippet'] = FeaturedSnippet(soup)

    did_you_mean = soup.select_one(Constants.SELECTORS.DID_YOU_MEAN)
    results['did_you_mean'] = did_you_mean.text if did_you_mean else None

    results['weather'] = Weather(soup, response.content)
    results['time'] = Time(soup) if not results['weather'].location else None
    results['location'] = Location(soup) if not results['time'] or not results['time'].hours else None

    results['dictionary'] = Dictionary(soup)
    results['translation'] = Translation(soup)
    results['top_stories'] = TopStories.parse(soup)
    results['unit_converter'] = Converters(soup)
    results['people_also_ask'] = PAA.parse(soup, response.content)
    results['people_also_search'] = PAS.parse(soup)

    return results


def upload_image(buffer, axios_config):
    form_data = {'encoded_image': buffer}
    headers = {'content-type': 'application/json', **Utils.get_headers(mobile=True)}
    response = requests.post(f"{Constants.URLS.GIS}searchbyimage/upload", json=form_data, headers=headers,
                             **axios_config)
    return response


def image(query, options={}):
    safe = options.get('safe', False)
    additional_params = options.get('additional_params', {})
    axios_config = options.get('axios_config', {})

    payload = [
        [
            [
                'HoAMBc',
                json.dumps([
                    None, None, [0, None, 2529, 85, 2396, [], [9429, 9520], [194, 194], False, None, None, 9520],
                    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                    None, None, None, None, None, None, None, None, None, [query], None, None, None, None, None,
                    None, None, None, [None, 'CAE=', 'GGwgAA=='], None, True
                ]),
                None,
                'generic'
            ]
        ]
    ]

    form_data = {'f.req': json.dumps(payload), 'at': f"{Utils.generate_random_string(29)}:{int(time.time())}"}
    if safe:
        additional_params['safe'] = 'active'

    params = {
        **additional_params,
        'rpcids': 'HoAMBc',
        'source-path': '/search',
        'f.sid': -random.randint(0, 9e10),
        'bl': 'boq_visualfrontendserver_20220505.05_p0',
        'hl': 'en',
        'authuser': 0,
        '_reqid': -random.randint(0, 9e5),
    }

    headers = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', **Utils.get_headers(mobile=False)}
    response = requests.post(f"{Constants.URLS.W_GOOGLE}_/VisualFrontendUi/data/batchexecute", data=form_data,
                             params=params, headers=headers, **axios_config)

    if response.status_code != 200:
        raise Utils.SearchError('Could not execute search', status_code=response.status_code)

    res = '[null' + (Utils.get_string_between_strings(response.content, '"[null', ']"') or '') + ']'
    data = json.loads(res.replace(r'\\"', "'"))

    if len(data) <= 1:
        raise Utils.SearchError('Got unexpected response from BatchExecute API', data)

    if not data[56][1]:
        raise Utils.SearchError(data[53][1] if data[53][1] else 'Unexpected response structure',
                                data[53][2] if data[53][2] else data)

    items = data[56][1][0][0][1][0]
    if not items:
        raise Utils.SearchError('Unexpected response structure', data)

    results = []
    for el in items:
        item = el[0][0]['444383007']
        if not item[1]:
            continue

        image_data = list(filter(lambda x: isinstance(x, list), item[1]))
        image = image_data[1]
        preview = image_data[0]
        origin = next((el for el in item[1] if el and el.get('2001')), None)

        if image and preview and origin:
            results.append({
                'id': item[1][1],
                'url': json.loads('"' + image[0].replace('"', '\\"') + '"'),
                'width': image[1],
                'height': image[2],
                'color': item[1][6],
                'preview': {
                    'url': json.loads('"' + preview[0].replace('"', '\\"') + '"'),
                    'width': preview[1],
                    'height': preview[2],
                },
                'origin': {
                    'title': origin['2008'][1],
                    'website': {
                        'name': origin['2003'][12],
                        'domain': origin['2003'][17],
                        'url': origin['2003'][2],
                    },
                },
            })

    return results


def get_top_news(language='en', region='US'):
    url = f"{Constants.URLS.GOOGLE_NEWS}topstories?tab=in&hl={language.lower()}-{region.upper()}&gl={region.upper()}&ceid={region.upper()}:{language.lower()}"
    response = requests.get(url, headers=Utils.get_headers(mobile=True))

    if response.status_code != 200:
        raise Utils.SearchError('Could not retrieve top news: ' + response.text)

    soup = BeautifulSoup(response.content, 'html.parser')
    headline_stories_publishers = [el.text for el in soup.select(Constants.SELECTORS.PUBLISHER)]
    headline_stories_imgs = [el['src'] for el in soup.select(Constants.SELECTORS.STORY_IMG)]
    headline_stories_time = [el.text for el in soup.select(Constants.SELECTORS.STORY_TIME)]

    results = {'headline_stories': []}
    for i, el in enumerate(soup.select(Constants.SELECTORS.STORY_TITLE)):
        headline_stories_title = el.text
        headline_stories_url = Constants.URLS.GOOGLE_NEWS + el['href'][2:]

        results['headline_stories'].append({
            'title': headline_stories_title,
            'url': headline_stories_url,
            'image': headline_stories_imgs[i],
            'published': headline_stories_time[i],
            'by': headline_stories_publishers[i],
        })

    return results
