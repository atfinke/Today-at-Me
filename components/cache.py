from datetime import datetime
import json

from configuration import config

def content(cache_dict, lifetime, request_from_server):
    if cache_dict:
        date = cache_dict[config.CACHE_DATE_KEY]

        now = datetime.now().timestamp()
        if request_from_server and now > date + (lifetime * config.CACHE_EARLY_SERVER_REFRESH_MULTIPLIER):
            return None
        elif now < date + lifetime:
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



def save(content, path):
    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: content
    }
    with open(path, 'w', encoding='utf-8') as data:
        json.dump(cache_dict, data)
    return cache_dict
