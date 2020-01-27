from datetime import datetime
import json

from configuration import config

def content(cache_dict, lifetime):
    if cache_dict:
        date = cache_dict[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + lifetime:
            return cache_dict[config.CACHE_CONTENT_KEY]
        else:
            return None
    else:
        return None

def fetch(path):
    try:
        with open(path) as data:
            cache = json.load(data)
            return cache
    except:
        pass


def save(cache_dict, path):
    with open(path, 'w', encoding='utf-8') as data:
        json.dump(cache_dict, data)
