import urllib.request, json 
from datetime import datetime

from components import cache, logging
from configuration import config

logger = logging.setup_logger(
    'theme-park', config.THEME_PARKS_LOGGING_PATH)
memory_cache = None

def fetch_wait_times():
    global memory_cache
    logger.info('fetch_wait_times: called')

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_wait_times: checking memory cache')
    else:
        logger.info('fetch_wait_times: checking disk cache')
        existing_cache = cache.fetch(config.THEME_PARKS_CACHE_PATH)

    content = cache.content(existing_cache, config.THEME_PARKS_CACHE_LIFETIME)
    if content:
        return content

    rides = []
    with urllib.request.urlopen(config.THEME_PARKS_DLR_URL) as url:
        for park_rides in list(json.loads(url.read().decode()).values()):
            rides.extend(park_rides)
    with urllib.request.urlopen(config.THEME_PARKS_WDW_URL) as url:
        for park_rides in list(json.loads(url.read().decode()).values()):
            rides.extend(park_rides)

    logger.info('fetch_wait_times: got {} rides'.format(len(rides)))
 
    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: rides
    }

    cache.save(cache_dict, config.THEME_PARKS_CACHE_PATH)
    memory_cache = cache_dict
    return rides